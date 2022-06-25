from django.urls import path
from . import views

app_name = 'web'

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.Find, name='search'),
    path('privacy', views.privacy, name='privacy'),
    path('about/', views.aboutus, name='about_us'),
    path('contact/', views.contactus, name='contact_us'),
    path('contactview', views.contactview, name='contactform'),
    path('community/', views.community, name='community'),
]