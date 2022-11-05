from rest_framework import serializers

class ProductCreateSerializer(serializers.Serializer):
    images = serializers.ListField(child=serializers.CharField())

class PriceCreateSerializer(serializers.Serializer):
    currency = serializers.CharField()
    sub_interval = serializers.CharField()
    unit_amount = serializers.IntegerField()

class CouponCreateSerializer(serializers.Serializer):
    percent_off = serializers.IntegerField()