from django.db import models
from django.core.exceptions import ValidationError

from user.models import User
from organisation.models import Organisation

def validate_phone_no(value):
    if not value.isdigit() or len(value) != 10:
       raise ValidationError("invalid phone number")

class Event(models.Model):
    name = models.CharField(max_length=30)
    logo_pic = models.CharField(max_length=100)
    email = models.EmailField()
    is_groups = models.BooleanField()
    website = models.CharField(max_length=100)
    TYPE_CHOICES = (
        ('O', 'Online'),
        ('F', 'Offline'),
        ('H', 'Hybrid'),
    )
    type = models.CharField(max_length=1,choices=TYPE_CHOICES)
    location = models.CharField(max_length=100,null=True)
    contact_no = models.CharField(max_length=10,validators=[validate_phone_no])
    organisation = models.ForeignKey(Organisation,on_delete=models.CASCADE,related_name='event')
    reg_close_time = models.DateTimeField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

class Participant(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='participant')
    event = models.ForeignKey(Event,on_delete=models.CASCADE,related_name='participants')


