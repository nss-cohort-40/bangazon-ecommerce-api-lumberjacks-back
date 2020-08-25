"""This file contains the Model for Customer"""

from django.db import models
from django.db.models import F
from django.contrib.auth.models import User

class Customer(models.Model):

    """This is the class that defines the Customer Model for the Bangazon eCommerce application"""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=95)
    phone_number = models.CharField(max_length=10)

    class Meta:
        ordering = (F('user.date_joined').asc(nulls_last=True),)
