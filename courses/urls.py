from django.urls import path, include
from .views import *

app_name = 'courses'

urlpatterns = [
    path('', index, name='home'),
    path('change-cart/', toggle_item_in_cart, name='toggle-item-in-cart'),
    path('courses_detail/<slug:slug>/', CourseDetailView.as_view(), name='course-details'),
    path('category/<slug:slug>/', CoursesByCategoryListView.as_view(),
         name='course-by-category'),
    path('cart/', CartView.as_view(), name='cart'),     
     path('checkout/', include([
     path('course/<slug:course_slug>/',
            checkout, name='course-checkout'),
     path('cart/', checkout, name='cart-checkout')
    ])),
    path('place_order/',place_order, name='place-order'),
    path('handlerequest/', handleRequest, name='handle-paytm-request'),

]
