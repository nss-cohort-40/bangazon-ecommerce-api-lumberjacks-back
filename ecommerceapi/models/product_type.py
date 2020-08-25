"""This file contains the Model for ProductType"""
from django.db import models


class ProductType(models.Model):

    """This class defines the ProductTypes for the Bangazon eCommerce application """

    name = models.CharField(max_length=50)

    class Meta:
        ordering = ("name",)
        verbose_name = ("Product_Type")
        verbose_name_plural = ("Product_Types")

    def __str__(self):
        return self.name
