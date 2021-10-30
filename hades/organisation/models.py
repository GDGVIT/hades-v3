from django.db import models
from user.models import User

class Organisation(models.Model):
    name = models.CharField(max_length=30)
    logo_pic = models.CharField(max_length=100)
    email = models.EmailField()
    website = models.CharField(max_length=100)
    contact_no = models.CharField(max_length=10)

class Member(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user')
    organisation = models.ForeignKey(Organisation,on_delete=models.CASCADE,related_name='organisation')
    role = models.CharField(max_length=10)

