from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse
from shop.models import Product
from courses.models import Course


class StaticSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return ['web:home', 'web:contact_us', 'web:about_us', 'web:community', 'shop:home']

    def location(self, item):
        return reverse(item)


class ProductSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return Product.objects.all()


class CourseSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return Course.objects.all()
