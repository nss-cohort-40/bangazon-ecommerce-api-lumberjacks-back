"""View module for handling requests about products"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rest_framework.decorators import action
from ecommerceapi.models import Product, Customer, ProductType

class ProductSerializer(serializers.HyperlinkedModelSerializer):
    '''Json serializer for products
        
        Arguments: 
            serializers
    '''
    class Meta: 
        model = Product
        url = serializers.HyperlinkedIdentityField(
            view_name='product',
            lookup_field='id'
        )
        fields = ('id', 'url', 'title', 'customer_id', 'customer', 'price', 'description', 'quantity', 'location', 'image', 'created_at', 'product_type' )

class Products(ViewSet):
    '''Products for Bangazon Ecommerce Site'''

    def create(self, request):
        '''Handle POST operations
        
        Returns:
            Response -- JSON serialized Product instance
        '''

        new_product = Product()
        customer = Customer.objects.get(user=request.auth.user)
        product_type = ProductType.objects.get(pk=request.data['product_type_id'])

        new_product.title = request.data['title']
        new_product.customer = customer
        new_product.price = request.data['price']
        new_product.description = request.data['description']
        new_product.quantity = request.data['quantity']
        new_product.location = request.data['location']
        new_product.image = request.data['image']
        new_product.created_at = request.data['created_at']
        new_product.product_type = product_type

        new_product.save()

        serializer = ProductSerializer(new_product, context={'request': request})

        return Response(serializer.data)
