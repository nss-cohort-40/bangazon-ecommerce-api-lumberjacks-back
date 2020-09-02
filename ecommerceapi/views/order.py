"""View module for handling requests about orders"""
from datetime import datetime
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
        fields = (
            'id',
            'url',
            'products',
            'customer_id',
            'customer',
            'payment_type_id',
            'created_at'
        )

class Orders(ViewSet):
    '''Orders for Bangazon eCommerce site.'''

    def create(self, request):
        '''
        Handle POST request for orders
        Returns:
            Response -- JSON serialized product instance
        '''
        #if user has order where payment type = null
        #then post to OrderProducts(orderID)
        #else run this
        #then post to OrderProducts with new OrderID

        current_user = Customer.objects.get(user=request.auth.user)
        try:
            open_order = Order.objects.get(customer=current_user, payment_type=None)
            product = Product.objects.get(pk=request.data['product_id'])

            order_product = OrderProduct()
            order_product.order = open_order
            order_product.product = product

            order_product.save()

            serializer = OrderProductSerializer(
                order_product, context={'request': request}
            )
            return Response(serializer.data)


                # return Response(serializer.data)

        except Order.DoesNotExist:
            new_order = Order()
            new_order.customer = current_user
            new_order.save()

            serializer = OrderSerializer(
                new_order, context={'request': request}
            )

            last_order_id = Order.objects.latest('id')
            new_order_product = OrderProduct()
            new_order_product.order = last_order_id
            new_order_product.product = product

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
        if pk is not None:
            order = Order.objects.get(pk=pk)
            serializer = OrderSerializer(
                order, context={'request': request}
            )
            return Response(serializer.data)
        else:
            current_user = Customer.objects.get(user=request.auth.user)
            try:
                order = Order.objects.get(customer=current_user, payment_type=None)
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
        order.id = request.data['id']
        order.created_at = datetime.today().strftime('%Y-%m-%d')
        order.customer_id = request.data['customer_id']
        order.payment_type_id = request.data['payment_type_id']
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
        orders = Order.objects.filter(customer=customer, payment_type=None)
        serializer = OrderSerializer(
            orders, many=True, context={'request': request}
        )
        return Response(serializer.data)
