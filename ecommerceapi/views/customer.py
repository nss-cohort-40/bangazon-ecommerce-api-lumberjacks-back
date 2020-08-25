"""View module for handling requests about customers"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from ecommerceapi.models import Customer

class CustomerSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for products.
    Arguments:
        serializers
    """

    class Meta:
        model = Customer
        url = serializers.HyperlinkedIdentityField(
            view_name="customer",
            lookup_field="id"
        )
        fields = (
            "id",
            "user",
            "address",
            "phone_number"
        )

class Customers(ViewSet):
    """Customers who visit the Bangazon eCommerce site."""

    def retrieve(self, request, pk=None):
        """Handle GET requests for single customers
        Returns:
            Response -- JSON serialized customer instance
        """

        try:
            customer = Customer.objects.get(pk=pk)
            serializer = CustomerSerializer(customer, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)