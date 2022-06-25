from django.db import models
from courses.models import Course
from shop.models import Product
from django.core.validators import MinValueValidator,MaxValueValidator



class Coursecoupon(models.Model):
    Ccode = models.CharField(max_length=50, unique=True)
    discount = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(100)])
    active = models.BooleanField(default=False)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()

    def __str__(self):
        return self.Ccode

class Shopcoupon(models.Model):
    Scode = models.CharField(max_length=50, unique=True)
    discount = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(100)])
    active = models.BooleanField(default=False)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()

    def __str__(self):
        return self.Scode