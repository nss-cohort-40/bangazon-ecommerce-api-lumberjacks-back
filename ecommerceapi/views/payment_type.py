"""View module for handling requests about payment types"""
from django.http import HttpResponseServerError
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from ecommerceapi.models import PaymentType, Customer

class PaymentTypeSerializer(serializers.HyperlinkedModelSerializer):
    """Payment type serializer"""

    class Meta:
        model = PaymentType
        url = serializers.HyperlinkedIdentityField(
            view_name="payment_type",
            lookup_field="id"
        )

        fields = (
            "id",
            "merchant_name",
            "account_number",
            "expiration_date",
            "created_at",
            "customer"
        )

class PaymentTypes(ViewSet):
    """
    View set class for payment types.
    """

    def retrieve(self, request, pk=None):
        """Handle GET requests for single payment type
        Returns:
            Response -- JSON serialized product instance
        """

        try:
            payment_type = PaymentType.objects.get(pk=pk)
            customer = Customer.objects.get(user=request.user)
            serializer = PaymentTypeSerializer(payment_type, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def create(self, request):
        '''Handle POST operations

        Returns:
            Response -- JSON serialized payment type instance
        '''

        new_pay_type = PaymentType()
        customer = Customer.objects.get(user=request.user)

        new_pay_type.merchant_name = request.data['merchantName']
        new_pay_type.account_number = request.data['accountNumber']
        new_pay_type.expiration_date = request.data['expirationDate']
        new_pay_type.customer = customer

        new_pay_type.save()

        serializer = PaymentTypeSerializer(new_pay_type, context={'request': request})

        return Response(serializer.data)

    def destroy(self, request, pk=None):
        '''
        Handle DELETE requests for a payment type. Django safedelete is active for this model.
        
        Returns:
            Response -- 200, 404, or 500 status code
        '''
        try:
            payment_type = PaymentType.objects.get(pk=pk)

            payment_type.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except PaymentType.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        '''Handle GET operations

        Returns:
            Response -- JSON serialized payment type instance
        '''

        payment_types = PaymentType.objects.all()

        current_user = Customer.objects.get(user=request.auth.user)

        new_payment_types = payment_types.filter(customer=current_user)

        serializer = PaymentTypeSerializer(
            new_payment_types, many=True, context={'request': request}
        )

        return Response(serializer.data)
