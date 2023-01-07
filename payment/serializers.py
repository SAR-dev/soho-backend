from rest_framework import serializers
from .models import Payment
from base_serializers import UserSerializer, GroupSerializer, ImageSerializer, CategorySerializer

class ProductCreateSerializer(serializers.Serializer):
    images = serializers.ListField(child=serializers.CharField())

class PriceCreateSerializer(serializers.Serializer):
    currency = serializers.CharField()
    sub_interval = serializers.CharField()
    unit_amount = serializers.IntegerField()

class CouponCreateSerializer(serializers.Serializer):
    percent_off = serializers.IntegerField()

class PaymentSerializer(serializers.ModelSerializer):
    payor = UserSerializer()
    payee = UserSerializer()
    class Meta:
        model = Payment
        fields = ['id','payor', 'payee', 'amount', 'currency', 'interval', 'created_at', 'updated_at']