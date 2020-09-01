"""This file contains the Model for Order"""

from django.db import models
from .customer import Customer
from .payment_type import PaymentType

class Order(models.Model):
    
    """This is the Model for a Order for the Bangazon eCommerce application"""

    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING, related_name='orders')
    payment_type = models.ForeignKey(PaymentType, on_delete=models.DO_NOTHING, related_name='orders', blank=True, null=True)
    created_at = models.DateField(blank=True, null=True)
    products = models.ManyToManyField("Product", through=("OrderProduct"))

    class Meta:
        verbose_name = ("Order")
        verbose_name_plural = ("Orders")

    def __str__(self):
        return f'Date this order was placed {self.created_at}'
