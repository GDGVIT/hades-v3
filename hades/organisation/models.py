from django.db import models
from django.core.exceptions import ValidationError
from user.models import User

def validate_phone_no(value):
    if not value.isdigit() or len(value) != 10:
       raise ValidationError("invalid phone number")

class Organisation(models.Model):
    name = models.CharField(max_length=30)
    logo_pic = models.CharField(max_length=100)
    email = models.EmailField()
    website = models.CharField(max_length=100)
    contact_no = models.CharField(max_length=10,validators=[validate_phone_no])

class Member(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='member')
    organisation = models.ForeignKey(Organisation,on_delete=models.CASCADE,related_name='member')
    role = models.CharField(max_length=10)

    class Meta:
        unique_together = ('user','organisation')

