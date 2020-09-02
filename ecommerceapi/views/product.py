"""View module for handling requests about products"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rest_framework.decorators import action
from ecommerceapi.models import Product, Customer, ProductType, Order, OrderProduct
    
class ProductSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for products.
    Arguments:
        serializers
    """

    class Meta:
        model = Product
        url = serializers.HyperlinkedIdentityField(
            view_name="product",
            lookup_field="id"
        )
        fields = (
            "id",
            "title",
            "customer",
            "customer_id",
            "price",
            "description",
            "quantity",
            "location",
            "image",
            "created_at",
            "product_type",
            "product_type_id",
        )

class Products(ViewSet):
    """Individual products for Bangazon eCommerce site."""

    def retrieve(self, request, pk=None):
        """Handle GET requests for single products
        Returns:
            Response -- JSON serialized product instance
        """

        try:
            product = Product.objects.get(pk=pk)
            product_type = ProductType.objects.get(pk=product.product_type_id)
            product.product_type__id = product_type.id
            serializer = ProductSerializer(product, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

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


    def list(self, request):
        """Handle GET requests for all products
        Returns:
            Response -- JSON serialized list of product instances
        """

        products = Product.objects.all()

        last_twenty_products = products[:20]

        myproducts = self.request.query_params.get('myproducts', None)
        title = self.request.query_params.get('title', None)
        if title is not None:
            products = products.filter(title__startswith=title)

            serializer = ProductSerializer(
                products, many=True, context={'request': request}
            )
            return Response(serializer.data)
        elif myproducts is not None:
            customer = Customer.objects.get(user=request.auth.user)
            products = products.filter(customer=customer)
            for product in products:
                orderproducts = OrderProduct.objects.filter(product=product)
                i = 0
                for orderproduct in orderproducts:
                    if orderproduct.order.payment_type is not None:
                        i = i + 1
                product.location = f"{product.location} $$${i}"

            serializer = ProductSerializer(
                products, many=True, context={'request': request}
            )
            return Response(serializer.data)
        else:

            serializer = ProductSerializer(
                last_twenty_products, many=True, context={'request': request}
            )
            return Response(serializer.data)

    @action(methods=['get', 'post', 'put'], detail=False)
    def cart(self, request, pk=None):
        current_user = Customer.objects.get(user=request.auth.user)
        if request.method == "GET": 
            #if user does not have an Order where paymenttype = null then create Order()
            #or do nothing / message/ redirect
            try:
                open_order = Order.objects.get(customer=current_user, payment_type=None)
                products_on_order = Product.objects.filter(cart__order=open_order)
            except Order.DoesNotExist as ex:
                return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

            serializer = ProductSerializer(products_on_order, many=True, context={'request': request})
            return Response(serializer.data)
        #delete product from cart
        elif request.method == 'PUT':
            product = request.data['product_id']
            open_order = Order.objects.get(customer=current_user, payment_type=None)
            product_order = OrderProduct.objects.filter(product_id=product, order=open_order)
            product_order[0].delete()
            return Response({}, status=status.HTTP_204_NO_CONTENT) 



