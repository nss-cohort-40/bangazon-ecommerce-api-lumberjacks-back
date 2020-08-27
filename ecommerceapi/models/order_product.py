"""This file contains the Model for OrderProduct"""

from django.db import models
from .order import Order
from .product import Product

class OrderProduct(models.Model):

    """This is the Model for Order Product for the Bangazon eCommerce application"""

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="cart")
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING, related_name="cart")

    class Meta:
        verbose_name = ("Order_Product")
        verbose_name_plural = ("Order_Products")

    def __str__(self):
        return self.product.title
       