"""View module for handling requests about users"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from ecommerceapi.models import Customer

class UserSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for currently logged in user.
    Arguments:
        serializers
    """

    class Meta:
        model = Customer
        url = serializers.HyperlinkedIdentityField(
            view_name="user",
            lookup_field="id"
        )
        fields = (
            "id",
            "address",
            "phone_number",
            "username",
            "first_name",
            "last_name",
            "email",
            "date_joined"
        )

class Users(ViewSet):
    """Users who visit the Bangazon eCommerce site."""

    def retrieve(self, request, pk=None):
        """Handle GET requests for current user
        Returns:
            Response -- JSON serialized customer instance
        """

        try:
            serializer = UserSerializer(customers, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)