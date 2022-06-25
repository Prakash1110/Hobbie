from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import DetailView, ListView
from django.http import HttpResponseForbidden
from courses.models import Course, Category, Cart
from .models import CourseOrder, EnrolledCourse, Question, QuizTaker, SelectedChoice
from .forms import ChoiceForm, ButtonForm, PlaceOrderForm
from shop.forms import ChangeCart
from django.contrib import messages
from web.models import Team
from django.views.generic import DetailView, FormView, View, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from paytm import Checksum
from website.settings import MID_PAYTM, MKEY_PAYTM
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse_lazy, reverse
import json
import requests
import datetime

def index(request):
    teams = Team.objects.all()
    courses = Course.objects.all()
#    top_courses = self.model.objects.all().order_by('?')
    return render(request, 'courses/index.html', {
        'teams': teams,
        'courses': courses,
        #      'top_courses':top_courses
    })


class CourseDetailView(DetailView):
    model = Course
    template_name = 'courses/detail.html'
    context_object_name = 'course'

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        slug = self.kwargs.get(self.slug_url_kwarg)
        slug_field = self.get_slug_field()
        queryset = queryset.filter(**{slug_field: slug})
        try:
            # Get the single item from the filtered queryset
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404("No %(verbose_name)s found matching the query" %
                          {'verbose_name': self.model._meta.verbose_name})
        print(obj)
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.get_object(self.get_queryset())
        context['slug'] = self.kwargs.get('slug')
        if self.request.user.is_authenticated:
            context['cart_form'] = ChangeCart()
            if EnrolledCourse.objects.filter(course=course, user_id=self.request.user.id).exists():
                context['is_enrolled'] = True
            else:
                cart = Cart(self.request)
                context['is_in_cart'] = cart.has_course(course)
        return context


def toggle_item_in_cart(request):
    if request.method == "POST" and request.is_ajax and request.user.is_authenticated:
        is_added = False
        form = ChangeCart(request.POST)
        user_cart = None
        course = None
        if form.is_valid():
            itemid = form.cleaned_data["itemid"]
            course = get_object_or_404(Course, pk=itemid)
            user_cart, _ = Cart.objects.get_or_create(user=request.user)
            if Cart.objects.filter(items_in_cart__pk=itemid, user=request.user).exists():
                user_cart.items_in_cart.remove(course)
                user_cart.number_of_items = user_cart.number_of_items - 1
                user_cart.save()
                is_added = False
            else:
                user_cart.items_in_cart.add(course)
                is_added = True
                user_cart.number_of_items = user_cart.number_of_items + 1
                user_cart.save()
            print(user_cart.number_of_items)
        return JsonResponse({
            "added_in_cart": is_added,
            "course_button_id": f'course-id-js-{course.pk}',
            "course_id": course.pk,
            "number_of_items": user_cart.number_of_items}, status=200)
    else:
        return HttpResponseForbidden()


class CartView(LoginRequiredMixin, ListView):
    model = Cart
    template_name = 'courses/cart.html'
    context_object_name = 'items_in_cart'


    def get_queryset(self):
        user_cart, _ = Cart.objects.get_or_create(user=self.request.user)
        items_in_cart = user_cart.items_in_cart.all()
        return items_in_cart

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart_form'] = ChangeCart()
        return context


@login_required
def place_order(request):
    course_slug = None
    if request.POST:
        form = PlaceOrderForm(request.POST)
        if form.is_valid():
            course_slug = form.cleaned_data['course_slug']
        else:
            print(form.errors)
            return HttpResponse(form.errors)
    else:
        HttpResponseForbidden()
    if course_slug:
        course = get_object_or_404(Course, slug=course_slug)
        hist = EnrolledCourse.objects.create(course=course,
                                             buy_price=course.price, user=request.user)

        order = CourseOrder()
        order.user = request.user
        order.total = hist.buy_price
        order.save()
        order.courses_enrolled.add(hist)

    else:
        user_cart, _ = Cart.objects.get_or_create(user=request.user)
        courses = user_cart.items_in_cart.all()

        order = CourseOrder()
        order.user = request.user
        order.total = 0
        hists = []
        for course in courses:
            hist = EnrolledCourse(
                course=course, buy_price=course.price, user=request.user)
            hist.save()
            hists.append(hist)
            order.total += hist.buy_price
        order.save()
        order.courses_enrolled.add(*hists)
        user_cart.number_of_items = 0
        user_cart.items_in_cart.clear()
        user_cart.save()

    # orderId = order.pk
    orderId = "co-"+str(order.pk)
    amount = order.total
   
    # Request paytm for amount from user to our merchant account

    paytmParams = dict()

    paytmParams["body"] = {
        "requestType"   : "Payment",
        "mid"           : MID_PAYTM,
        "websiteName"   : "WEBSTAGING",
        "orderId"       : orderId,
        "callbackUrl"   : request.build_absolute_uri(reverse('courses:handle-paytm-request')),
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
        return render(request, 'courses/paytm.html', params)   

    messages.success(request, response['body']['resultInfo']['resultMsg'])
    return redirect("courses:home")



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
    order = CourseOrder.objects.get(pk = order_id)

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

    return render(request, 'courses/paymentstatus.html', response_dict)


    

@login_required
def checkout(request, course_slug=None):
    course, courses, num_items = None, None, None
    if course_slug:
        course = get_object_or_404(Course, slug=course_slug)
        num_items = 1
    else:
        user_cart, _ = Cart.objects.get_or_create(user=request.user)
        courses = user_cart.items_in_cart.all()
        num_items = courses.count()
    course_list = courses or (course,)
    total_price = 0
    if course:
        total_price =  course.price
    elif courses:
        price_list = course_list.values_list('price')
        for price, in price_list:
            total_price += price
    else:
        return redirect('course:home')
    form = PlaceOrderForm()
    form.fields['course_slug'].initial = course_slug
    return render(request, 'courses/checkout.html', {
        'is_course': True if course_slug else False,
        'courses': course_list,
        'total_price': total_price,
        'number_of_items': num_items,
        'form': form
    })


class CoursesByCategoryListView(ListView):
    model = Course
    template_name = 'courses/courses_by_category.html'
    context_object_name = 'courses'

    def get_queryset(self):
        category = Category.objects.get(slug=self.kwargs['slug'])
        return self.model.objects.filter(category_id=category.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = Category.objects.get(slug=self.kwargs['slug'])
        context['category'] = category
        context['categories'] = Category.objects.all()
        return context
