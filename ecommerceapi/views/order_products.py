"""View module for handling requests about orders"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from ecommerceapi.models import Product, Customer, Order, OrderProduct

class OrderProductSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for order product

    Arguments:
        serializers
    """
    class Meta:
        model = OrderProduct
        url = serializers.HyperlinkedIdentityField(
            view_name='order_product',
            lookup_field='id'
        )
        fields = ('id', 'url', 'order_id', 'order', 'product_id', 'product')
        depth = 2
        

class OrderProducts(ViewSet):
    '''Order Products for Bangazon eCommerce site.'''

    def create(self, request):
        '''
        Handle POST request for order products
        Returns:
            Response -- JSON serialized product instance
        '''

        new_order_product = OrderProduct()
        new_order_product.order_id = request.data['order_id']
        new_order_product.product_id = request.data['product_id']
        new_order_product.save()

        serializer = OrderProductSerializer(
            new_order_product, context={'request': request}
        )
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        '''
        Handle Get request for single orders
        Returns:
            Response -- JSON serialized product instance
        '''
        try:
            order_product = OrderProduct.objects.get(pk=pk)
            serializer = OrderProductSerializer(
                order_product, context={'request': request}
            )
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def destroy(self, request, pk=None):
        '''
        Handle DELETE requests for a single order product
        Returns:
            Response -- 200, 404, or 500 status code
        '''
        try: 
            order_product = OrderProduct.objects.get(pk=pk)
            order_product.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)
        
        except OrderProduct.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        '''
        Handle GET requests to order resource
        Returns:
            Response -- JSON serialized list of customer orders
        '''
        order_product = OrderProduct.objects.all()
        serializer = OrderProductSerializer(
            order_product, many=True, context={'request': request}
        )
        return Response(serializer.data)

