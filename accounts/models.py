from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.files import File
from django.db import models
from .validators import validate_file_size
from phonenumber_field.modelfields import PhoneNumberField
from accounts.managers import UserManager
from PIL import Image
from io import BytesIO  
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys

def compress(image):
    img = Image.open(image)
    im_io = BytesIO()
    print(img.format)
    img.save(im_io, img.format, optimize=True, quality=40)
    new_image = File(im_io, name=image.name)
    return new_image

def has_changed(instance, field):
    if not instance.pk:
        return False
    old_value = instance.__class__._default_manager.\
    filter(pk=instance.pk).values(field).get()[field]
    return not getattr(instance, field) == old_value


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)



class User(AbstractUser):

    username = models.CharField(
        'username', unique=True, blank=False, max_length=10)
    # Identifiable Information
    first_name = models.CharField(
        'First Name', unique=False, blank=False, max_length=50)
    last_name = models.CharField(
        'Last Name', unique=False, blank=False, max_length=20)
    email = models.EmailField('email address', unique=True, blank=False)
    phone_number = PhoneNumberField(unique=True, null=True, blank=False)
    profile_photo = models.ImageField(
        null=True, blank=True, upload_to='profile_pics/', validators=[validate_file_size],default='/static/assets/images/image.png')
    is_teacher = models.BooleanField(default=False)
    is_seller = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()


    def save(self, *args, **kwargs):
        if has_changed(self, 'profile_photo'):
            self.profile_photo = compress(self.profile_photo)
        return super().save()
