from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from .managers import CustomUserManager
from django.conf import settings
from datetime import date

def validate_phone_no(value):
    if not value.isdigit() or len(value) != 10:
       raise ValidationError("invalid phone number")

class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique = True)
    phone_no = models.CharField(max_length = 10,null=True,validators=[validate_phone_no])
    profile_pic = models.CharField(max_length = 100,null=True)
    first_name = models.CharField(max_length=50,null=False)
    last_name = models.CharField(max_length=50,null=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [ 'first_name', 'last_name']
    objects = CustomUserManager()
    def __str__(self):
        return "{}".format(self.email)
