from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.


class ContactModel(models.Model):
    name = models.CharField(max_length=25)
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    phone = PhoneNumberField()
    message = models.TextField()

    def __str__(self):
        return self.name


class Team(models.Model):
    name = models.CharField(max_length=25)
    post = models.CharField(max_length=25)
    image = models.ImageField(null=True, blank=True,
                              upload_to='media/images/team')
    fb_url = models.CharField(null=True, blank=True, max_length=255)
    instagram_url = models.CharField(null=True, blank=True, max_length=255)
    twitter_url = models.CharField(null=True, blank=True, max_length=255)
    linkedin_url = models.CharField(null=True, blank=True, max_length=255)


class Project(models.Model):
    name = models.CharField(max_length=25)
    image = models.ImageField(upload_to='media/images/project')
    url = models.URLField(null=True)
