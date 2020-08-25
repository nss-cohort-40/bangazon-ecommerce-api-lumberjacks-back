"""View module for handling requests about product types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from ecommerceapi.models import ProductType

class ProductTypeSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for product types.
    Arguments:
        serializers
    """

    class Meta:
        model = ProductType
        url = serializers.HyperlinkedIdentityField(
            view_name="product_type",
            lookup_field="id"
        )
        fields = ("id", "url", "name")

class ProductTypes(ViewSet):
    """Product Types for Bangazon eCommerce site."""

    def retrieve(self, request, pk=None):
        """Handle GET requests for single product type
        Returns:
            Response -- JSON serialized product type instance
        """

        try:
            product_type = ProductType.objects.get(pk=pk)
            serializer = ProductTypeSerializer(product_type, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests for all product types
        Returns:
            Response -- JSON serialized list of product type instances
        """

        product_types = ProductType.objects.all()

        serializer = ProductTypeSerializer(
            product_types, many=True, context={'request': request}
        )
        return Response(serializer.data)
