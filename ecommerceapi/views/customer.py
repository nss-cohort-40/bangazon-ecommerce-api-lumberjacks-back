"""View module for handling requests about customers"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from ecommerceapi.models import Customer
from django.contrib.auth.models import User

class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        url = serializers.HyperlinkedIdentityField(
            view_name="user",
            lookup_field="id"
        )
        fields = (
            "id",
            "first_name",
            "last_name",
            "date_joined",
            "email"
        )

class CustomerSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for products.
    Arguments:
        serializers
    """

    user = UserSerializer()

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

    def update(self, request, pk=None):
        """Handle PUT requests for a customer

        Returns:
            Response -- Empty body with 204 status code
        """
        customer = Customer.objects.get(pk=pk)
        customer.address = request.data["address"]
        customer.phone_number = request.data["phoneNumber"]
        customer.save()

        user = User.objects.get(pk=customer.user.id)
        user.last_name = request.data["lastName"]
        user.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)
    
    def list(self, request):

        if request.user.id:
            customers = Customer.objects.filter(user=request.user.id)

        else:
            customers = Customer.objects.all()

        serializer = CustomerSerializer(
            customers, many=True, context={'request': request})

        return Response(serializer.data)