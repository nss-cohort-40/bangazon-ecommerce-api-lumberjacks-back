"""View module for handling requests about products"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rest_framework.decorators import action
from ecommerceapi.models import Product, Customer, ProductType
    
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
            "price",
            "description",
            "quantity",
            "location",
            "image",
            "created_at",
            "product_type"
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

        product_type = self.request.query_params.get('product_type', None)
        if product_type is not None:
            products = products.filter(product_type__id=product_type)

        serializer = ProductSerializer(
            last_twenty_products, many=True, context={'request': request}
        )
        return Response(serializer.data)
