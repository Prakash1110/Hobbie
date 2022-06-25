"""coffeehouse URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from shop.models import Product
from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.home, name='home'),
    path('change-cart/', views.toggle_item_in_cart, name='toggle-item-in-cart'),
    path('product-detail/<slug:product_slug>/',
         views.product_detail_page, name='product-detail'),
    path('cart/', views.cart, name='cart'),
    path('address_add/', views.add_address, name='add-address'),
    path('checkout/', include([
        path('product/<slug:product_slug>/',
             views.checkout, name='product-checkout'),
        path('cart/', views.checkout, name='cart-checkout')
    ])),
    path('place_order/', views.place_order, name='place-order'),
    path('handlerequest/', views.handleRequest, name='handle-paytm-request'),

]
