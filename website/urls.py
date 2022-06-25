"""website URL Configuration

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
from django.contrib import admin
from django.urls import path

from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.sitemaps import GenericSitemap
from django.contrib.sitemaps.views import sitemap

from website import settings
from website.sitemap import StaticSitemap, ProductSitemap, CourseSitemap

sitemaps = {
    'static': StaticSitemap,
    'products': ProductSitemap,
    'courses': CourseSitemap,
}

urlpatterns = [
    path('django-admin/', admin.site.urls),
#    path('cart/', include('cart.urls')),
    path('', include('accounts.urls')),
    path('accounts/', include('allauth.urls')),
    path('', include('web.urls')),
    path('course/', include('courses.urls', namespace='course')),
    path('shop/', include('shop.urls')),
    path('admin/shop/', include('shopAdmin.urls')),
    path('admin/course/', include('courseAdmin.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('djga/', include('google_analytics.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# handler404 = 'web.views.handler404'
# handler500 = 'web.views.handler500'
