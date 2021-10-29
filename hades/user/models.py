from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from .managers import CustomUserManager
from django.conf import settings
from datetime import date

class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique = True)
    phone_no = models.CharField(max_length = 10)
    profile_pic = models.CharField(max_length = 50,null=True)
    first_name = models.CharField(max_length=50,null=False)
    last_name = models.CharField(max_length=50,null=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [ 'first_name', 'last_name']
    objects = CustomUserManager()
    def __str__(self):
        return "{}".format(self.email)
