"""View module for handling requests about orders"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from ecommerceapi.models import Product, Customer, Order

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
        fields = ('id', 'url', 'customer_id', 'customer', 'payment_type_id', 'created_at')

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
        Handle Get request for single orders
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

    def update(self, request, pk=None):
        """Handle PUT requests for an individual order item

        Returns:
            Response -- Empty body with 204 status code
        """
        order = Order.objects.get(pk=pk)
        order.created_at = request.data["created_at"]
        order.save()
        
        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        '''
        Handle DELETE requests for a single order
        Returns:
            Response -- 200, 404, or 500 status code
        '''
        try: 
            order = Order.objects.get(pk=pk)
            order.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)
        
        except Order.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        '''
        Handle GET requests to order resource
        Returns:
            Response -- JSON serialized list of customer orders
        '''
        customer = Customer.objects.get(user=request.auth.user)
        orders = Order.objects.filter(customer=customer)
        serializer = OrderSerializer(
            orders, many=True, context={'request': request}
        )
        return Response(serializer.data)
