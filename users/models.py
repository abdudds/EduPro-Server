from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser
from django.core.validators import RegexValidator
from django.conf import settings

# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)
    
class User(AbstractUser):
    username = None
    name = models.CharField(max_length=250)
    email = models.CharField(max_length=250, unique=True)
    password = models.CharField(max_length=250)
    profile_img = models.ImageField(upload_to='profile', blank=True, default='profDefault.png')
    # mobile_regex = RegexValidator(regex=r'^\d+$', message="Mobile number should only contains didgits")
    # mobile = models.CharField(max_length=10, null=True, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    is_admin = models.BooleanField(default=False)
    is_tutor = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    @property
    def profile_img_url(self):
        if self.profile_img:
            return f"{settings.BASE_URL}{self.profile_img.url}"
        return ''

    def __str__(self):
        return self.email
    


