"""This file contains the Model for Product"""

from django.db import models
from .customer import Customer
from .product_type import ProductType

class Product(models.Model):

    """This class defines the Product for the Bangazon eCommerce application"""

    title = models.CharField(max_length=50)
    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.CharField(max_length=255)
    quantity = models.IntegerField()
    location = models.CharField(max_length=75)
    image = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now=True)
    product_type = models.ForeignKey(ProductType, on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = ("Product")
        verbose_name_plural = ("Products")

    def __str__(self):
        return self.title
