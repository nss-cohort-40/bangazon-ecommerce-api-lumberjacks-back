"""This file contains the Model for Customer"""

from django.db import models
from django.db.models import F
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

class Customer(models.Model):

    """This is the class that defines the Customer Model for the Bangazon eCommerce application"""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=95)
    phone_number = models.CharField(max_length=10)
        
    class Meta:
        ordering = (F('user.date_joined').asc(nulls_last=True),)

@receiver(post_save, sender=User)
def create_customer(sender, instance, created, **kwargs):
    if created:
        Customer.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_customer(sender, instance, **kwargs):
    instance.customer.save()
