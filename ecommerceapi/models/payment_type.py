"""This file contains the Model for PaymentType"""

from django.db import models
from .customer import Customer

class PaymentType(models.Model):

    """This class defines the payment types for the Bangazon eCommerce application"""

    merchant_name = models.CharField(max_length=25)
    account_number = models.CharField(max_length=25)
    expiration_date = models.DateTimeField(auto_now=True)
    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = ("Payment_Type")
        verbose_name_plural = ("Payment_Types")

    def __str__(self):
        return self.merchant_name
