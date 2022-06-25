from django.db.models.aggregates import Sum
from django.http.response import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponseForbidden
from web.forms import ContactForm
from .forms import AddAddressForm, ChangeCart, PlaceOrderForm
from .models import Product, Cart, ProductBuyHistory, ProductOrder
from django.contrib import messages
from website.settings import MID_PAYTM, MKEY_PAYTM
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse_lazy, reverse
from paytm import Checksum
import json
import requests
import datetime
# Create your views here.


def home(request):
    form = ContactForm()
    products = Product.objects.all()
    cart_form = ChangeCart()
    user_cart = None
    items_in_cart = None
    if request.user.is_authenticated:
        user_cart, _ = Cart.objects.get_or_create(user=request.user)
        print(user_cart)
        items_in_cart = user_cart.items_in_cart.all()
    return render(request, 'shop/index.html',
                  {
                      'form': form,
                      'products': products,
                      'cart_form': cart_form,
                      'cart': user_cart,
                      'items_in_cart': items_in_cart
                  })


def toggle_item_in_cart(request):
    if request.method == "POST" and request.is_ajax and request.user.is_authenticated:
        is_added = False
        form = ChangeCart(request.POST)
        user_cart = None
        product = None
        if form.is_valid():
            itemid = form.cleaned_data["itemid"]
            product = get_object_or_404(Product, pk=itemid)
            user_cart, _ = Cart.objects.get_or_create(user=request.user)
            if Cart.objects.filter(items_in_cart__id=itemid, user=request.user).exists():
                user_cart.items_in_cart.remove(product)
                user_cart.number_of_items = user_cart.number_of_items - 1
                user_cart.save()
                is_added = False
            else:
                user_cart.items_in_cart.add(product)
                is_added = True
                user_cart.number_of_items = user_cart.number_of_items + 1
                user_cart.save()
            print(user_cart.number_of_items)
        return JsonResponse({
            "added_in_cart": is_added,
            "product_button_id": f'product-id-js-{product.pk}',
            "product_id": product.pk,
            "number_of_items": user_cart.number_of_items}, status=200)
    else:
        return HttpResponseForbidden()


def product_detail_page(request, product_slug):
    items_in_cart = None
    user_cart = None
    if request.user.is_authenticated:
        user_cart, _ = Cart.objects.get_or_create(user=request.user)
        items_in_cart = user_cart.items_in_cart.all()
    return render(request, "shop/product_detail.html",
                  {
                      'cart_form': ChangeCart(),
                      'product': get_object_or_404(Product, slug=product_slug),
                      'items_in_cart': items_in_cart or None
                  })


@login_required
def cart(request):
    items_in_cart = None
    user_cart, _ = Cart.objects.get_or_create(user=request.user)
    print(user_cart)
    items_in_cart = user_cart.items_in_cart.all()

    return render(request, 'shop/cart.html', {
        'items_in_cart': items_in_cart,
        'cart_form': ChangeCart()
    })


@login_required
def checkout(request, product_slug=None):
    product, products, num_items = None, None, None
    if product_slug:
        product = get_object_or_404(Product, slug=product_slug)
        num_items = 1
    else:
        user_cart, _ = Cart.objects.get_or_create(user=request.user)
        products = user_cart.items_in_cart.all()
        num_items = products.count()
    product_list = products or (product,)
    total_price = 0
    if product:
        total_price = product.discounted_price or product.price
    elif products:
        for price, discounted_price in product_list.values_list('price', 'discounted_price'):
            total_price += discounted_price or price
    else:
        return redirect('shop:home')
    form = PlaceOrderForm(user=request.user)
    form.fields['product_slug'].initial = product_slug

    return render(request, 'shop/checkout.html', {
        'is_product': True if product_slug else False,
        'products': product_list,
        'total_price': total_price,
        'number_of_items': num_items,
        'form': form,
        'address_form': AddAddressForm()
    })


@login_required
def add_address(request):
    if request.is_ajax and request.POST and request.user.is_authenticated:
        form = AddAddressForm(request.POST)
        flag = False
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            flag = True
        return JsonResponse({'is_saved': flag}, status=200)
    else:
        return HttpResponseForbidden()


@login_required
def place_order(request):
    address, product_slug = None, None
    if request.POST:
        form = PlaceOrderForm(request.POST, user=request.user)
        if form.is_valid():
            address = form.cleaned_data['address']
            product_slug = form.cleaned_data['product_slug']
        else:
            print(form.errors)
            return HttpResponse(form.errors)
    else:
        HttpResponseForbidden()
    if product_slug:
        product = get_object_or_404(Product, slug=product_slug)
        hist = ProductBuyHistory.objects.create(product=product,
                                                buying_price=product.discounted_price or product.price)

        order = ProductOrder()
        order.user = request.user
        order.address = address
        order.total = hist.buying_price
        order.save()
        order.product_history.add(hist)

    else:
        user_cart, _ = Cart.objects.get_or_create(user=request.user)
        products = user_cart.items_in_cart.all()

        order = ProductOrder()
        order.user = request.user
        order.address = address
        order.total = 0
        hists = []
        for product in products:
            hist = ProductBuyHistory(
                product=product, buying_price=product.discounted_price or product.price)
            hist.save()
            hists.append(hist)
            order.total += hist.buying_price
        order.save()
        order.product_history.add(*hists)
        user_cart.number_of_items = 0
        user_cart.items_in_cart.clear()
        user_cart.save()
    
    # orderId = order.pk
    orderId = "pr-"+str(order.pk)
    amount = order.total
   
    # Request paytm for amount from user to our merchant account

    paytmParams = dict()

    paytmParams["body"] = {
        "requestType"   : "Payment",
        "mid"           : MID_PAYTM,
        "websiteName"   : "WEBSTAGING",
        "orderId"       : orderId,
        "callbackUrl"   : request.build_absolute_uri(reverse('shop:handle-paytm-request')),
        "txnAmount"     : {
            "value"     : str(amount),
            "currency"  : "INR",
        },
        "userInfo"      : {
            "custId"    : str(request.user.pk),
        },
    }

    # Generate checksum by parameters we have in body
    # Find your Merchant Key in your Paytm Dashboard at https://dashboard.paytm.com/next/apikeys 
    checksum = Checksum.generateSignature(json.dumps(paytmParams["body"]), MKEY_PAYTM)

    paytmParams["head"] = {
        "signature"    : checksum
    }
    # print(checksum) 
    post_data = json.dumps(paytmParams)
    # for staging
    url = f"https://securegw-stage.paytm.in/theia/api/v1/initiateTransaction?mid={MID_PAYTM}&orderId={orderId}"
    response = requests.post(url, data = post_data, headers = {"Content-type": "application/json"}).json()
    print(response)
    resCode = response['body']['resultInfo']['resultCode']
    params = {
        'mid' : MID_PAYTM,
        'orderId' : orderId
    }

    if(resCode == '0000'):
        # print(response['body']['txnToken'])
        params['txnToken'] = response['body']['txnToken']
        return render(request, 'shop/paytm.html', params)   

    messages.success(request, response['body']['resultInfo']['resultMsg'])
    return redirect("shop:home")


@csrf_exempt
def handleRequest(request):
    # paytm make post request here
    form = request.POST
    response_dict = {}
    for i in form.keys():
        if i == 'CHECKSUMHASH':
            checksum = form[i]
            continue
        response_dict[i] = form[i]
    
    order_id = response_dict['ORDERID']
    order_id = order_id[3:]
    order = ProductOrder.objects.get(pk = order_id)

    isChecksumVerified = Checksum.verifySignature(response_dict, MKEY_PAYTM, checksum)
    if isChecksumVerified:

        order.transaction_id = response_dict['TXNID']
        order.bank_id = response_dict['BANKTXNID']
        order.payment_status = 'SS'
        order.transaction_date = datetime.datetime.strptime(response_dict['TXNDATE'], '%Y-%m-%d %H:%M:%S.%f')
        order.transaction_resp_code = response_dict['RESPCODE']
        order.transaction_resp_msg = response_dict['RESPMSG']

        if response_dict['RESPCODE'] == '01':
            print('payment successfull')
            order.payment_status = 'SS'
            order.save()
            messages.success(request, "Your order has been Placed")
        else:
            order.payment_status = 'FF'
            order.save()
            print('payment failed due to ' + response_dict['RESPMSG'])

    return render(request, 'shop/paymentstatus.html', response_dict)
