import json
from rest_framework import status
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from ecommerceapi.models import Product, Customer, ProductType

class TestProduct(TestCase):

    def setUp(self):
        self.username = 'testuser'
        self.password = 'foobar'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.token = Token.objects.create(user=self.user)
        self.customer = Customer.objects.create(user=self.user, address='123 Street', phone_number="12322222")
        self.product_type = ProductType.objects.create(name='Electronics')

    def test_post_product(self):
        new_product = {
            "title": "test",
            "price": 20,
            "description": 'Testing Products',
            "quantity": 10,
            "location": 'Nashville, TN',
            "image": 'awesome image',
            "created_at": "04-13-2020",
            "product_type_id": self.product_type.id,
        }
        response = self.client.post(
            reverse('product-list'), new_product, HTTP_AUTHORIZATION='Token ' + str(self.token)
        )
        # Getting 200 back because we have a success url
        self.assertEqual(response.status_code, 200)

        # Query the table to see if there's one ParkArea instance in there. Since we are testing a POST request, we don't need to test whether an HTTP GET works. So, we just use the ORM to see if the thing we saved is in the db.
        self.assertEqual(Product.objects.count(), 1)

        # And see if it's the one we just added by checking one of the properties. Here, name.
        self.assertEqual(Product.objects.get().title, 'test')
