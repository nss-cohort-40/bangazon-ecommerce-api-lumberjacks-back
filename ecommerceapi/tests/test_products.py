"""Product testing module."""
import unittest
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from ecommerceapi.models import Product, Customer, ProductType
# from .views import <Why don't we need to do this?>

class TestProduct(TestCase):
    """
    Test class for Product viewset.
    """
    def setUp(self):
        self.username = "testuser"
        self.password = "foobar"
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.token = Token.objects.create(user=self.user)
        self.customer = Customer.objects.create(
            user=self.user,
            address="123 Whatever Street",
            phone_number="555-5555"
        )
        self.product_type = ProductType.objects.create(name="Electronics")

    def test_post_products(self):
        """Method for testing post requests for products."""
        new_product = {
            "title": "TV",
            "price": 30.00,
            "description": "Test",
            "quantity": 1,
            "location": "Nashville, TN",
            "image": "",
            "created_at": "2020-09-04",
            "product_type_id": 1
        }

        response = self.client.post(
            reverse('product-list'), new_product, HTTP_AUTHORIZATION='Token ' + str(self.token)
        )

        self.assertEqual(response.status_code, 200)

    def test_list_products(self):
        """Method for testing getting all products."""

        new_product = Product.objects.create(
            title="TV",
            customer_id=1,
            price=30.00,
            description="Test",
            quantity=1,
            location="Nashville, TN",
            image="",
            created_at="2020-09-04",
            product_type_id=1
        )

        new_product_two = Product.objects.create(
            title="Toaster",
            customer_id=1,
            price=40.00,
            description="Test",
            quantity=1,
            location="Nashville, TN",
            image="",
            created_at="2020-09-04",
            product_type_id=1
        )

        response = self.client.get(
            reverse('product-list')
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(response.data), 2)

        self.assertIn(new_product.title.encode(), response.content)

        self.assertIn(new_product_two.title.encode(), response.content)

    def test_delete_products(self):
        """Method for testing delete products."""

        new_product = Product.objects.create(
            title="TV",
            customer_id=1,
            price=30.00,
            description="Test",
            quantity=1,
            location="Nashville, TN",
            image="",
            created_at="2020-09-04",
            product_type_id=1
        )

        response = self.client.delete(
            reverse('product-list')
        )

        self.assertEqual(Product.objects.count(), 1)

        self.assertEqual(response.status_code, 200)
