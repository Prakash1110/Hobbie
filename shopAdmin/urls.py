from django.urls import path
from . import views
from .views import *

app_name = 'shopAdmin'

urlpatterns = [
    path('', views.home, name='home'),
    path('add_items/', views.add_items, name='add_items'),
    path('update/<int:pk>', UpdateItem.as_view(), name='update_item'),
    path('delete/<int:pk>', DeleteItem.as_view(), name='delete_item'),
]
