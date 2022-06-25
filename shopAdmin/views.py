from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView, DeleteView
from shop.models import Product, Category
from shopAdmin.forms import ProductForm


# Create your views here.
def home(request):
    products = Product.objects.all()
    return render(request, 'shopAdmin/dashboard.html', {'products': products})


def add_items(request):
    if request.POST:
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            pass
        else:
            print(form.errors)
        return redirect('shopAdmin:add_items')
    form = ProductForm()
    category = Category.objects.all()

    return render(request, "shopAdmin/add_items.html", {"category": category,
                                                        "form": form})


class UpdateItem(UpdateView):
    model = Product
    template_name = 'shopAdmin/update.html'
    fields = ['price', 'discounted_price', 'number_of_items', 'items_sold']
    success_url = '/admin/shop/'


class DeleteItem(DeleteView):
    model = Product
    template_name = 'shopAdmin/delete.html'
    success_url = reverse_lazy('shopAdmin:home')
