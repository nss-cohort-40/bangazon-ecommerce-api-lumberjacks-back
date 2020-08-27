"""View module for handling requests about payment types"""
from django.http import HttpResponseServerError
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from ecommerceapi.models import PaymentType, Customer

class PaymentTypeSerializer(serializers.HyperlinkedModelSerializer):

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

    def list(self, request):

        payment_types = PaymentType.objects.all()

        serializer = PaymentTypeSerializer(
            payment_types, many=True, context={'request': request}
        )

        return Response(serializer.data)

    @action(methods=['get'], detail=False)
    def userPay(self, request):
        current_user = Customer.objects.get(user=request.auth.user)

        user_pay_types = PaymentType.objects.all(customer=current_user)

        serializer = PaymentTypeSerializer(user_pay_types, many=True, context={'request': request})

        return Response(serializer.data)