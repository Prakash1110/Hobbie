from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone
from django.contrib.auth import get_user_model


# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField()

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=200)
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)
    price = models.IntegerField()
    discounted_price = models.IntegerField(blank=True)
    image = models.ImageField(upload_to='products/')
    slug = models.SlugField(unique=True, blank=True)
    items_sold = models.IntegerField(default=0)
    number_of_items = models.IntegerField(default=0)
    description = models.TextField()
    is_out_of_stock = models.BooleanField(default=False)
    date_added = models.DateTimeField(default=timezone.now)

    def save(self):
        self.slug = self.slug or slugify(self.title)
        super().save()

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('shop:product-detail', kwargs={"product_slug": self.slug})


class Cart(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='shop_cart')
    items_in_cart = models.ManyToManyField(Product, blank=True)
    number_of_items = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Cart"
        verbose_name_plural = "Carts"

    def __str__(self):
        return self.user.get_full_name()


class Address(models.Model):
    '''Model for handling multiple adresses of a user'''
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self) -> str:
        return self.text[:50] + '...'


class ProductBuyHistory(models.Model):
    '''Model to keep track of product buy history bought at a "then" price.'''
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    datetime = models.DateTimeField(default=timezone.now)
    buying_price = models.IntegerField()


class ProductOrder(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    address = models.ForeignKey(Address, null=True, on_delete=models.SET_NULL)
    total = models.IntegerField()
    product_history = models.ManyToManyField(ProductBuyHistory)
    payment_status = models.CharField(max_length=2, default='PN', choices=(
        ('PN', 'Pending'),
        ('SS', 'Successful'),
        ('FF', 'Failed')
    ))
    transaction_id = models.CharField(max_length=255, default="")
    bank_id = models.CharField(max_length=255, default="")
    transaction_date = models.DateTimeField(default=timezone.now)
    transaction_resp_code = models.CharField(max_length=50, default="")
    transaction_resp_msg = models.TextField(default="")
    