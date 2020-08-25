"""View module for handling requests about orders"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from ecommerceapi.models import Product, Customer, Order
from .product import ProductSerializer

class OrderSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for orders

    Arguments:
        serializers
    """
    class Meta:
        model = Order
        url = serializers.HyperlinkedIdentityField(
            view_name='order',
            lookup_field='id'
        )
        fields = ('id', 'url', 'customer_id', 'customer', 'payment_type_id' 'payment_type', 'created_at')

class Orders(ViewSet):
    '''Orders for Bangazon eCommerce site.'''

    def create(self,request):
        '''
        Handle POST request for orders
        Returns:
            Response -- JSON serialized product instance
        '''

        new_order = Order()
        new_order.customer_id = request.data['customer_id']
        new_order.payment_type_id = request.data['payment_type_id']
        new_order.save()

        serializer = OrderSerializer(
            new_order, context={'request': request}
        )
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        '''
        Handle Get request for orders
        Returns: 
            Response -- JSON serialized product instance
        '''
        try:
            order = Order.objects.get(pk=pk)
            serializer = OrderSerializer(
                order, context={'request': request}
            )
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self)     