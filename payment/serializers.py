from rest_framework import serializers

class ProductCreateSerializer(serializers.Serializer):
    images = serializers.ListField(child=serializers.CharField())

class PriceCreateSerializer(serializers.Serializer):
    currency = serializers.CharField()
    interval = serializers.CharField()
    cents_amount = serializers.IntegerField()

class CouponCreateSerializer(serializers.Serializer):
    amount_off = serializers.IntegerField()
    currency = serializers.CharField()