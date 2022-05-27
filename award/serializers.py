from rest_framework import serializers
from .models import Award

class AwardCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Award
        fields = ['id', 'name', 'description', 'logo', 'price']
        read_only_fields = ['price']

class AwardUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Award
        fields = ['id', 'name', 'description', 'logo', 'price']
        read_only_fields = ['price']
        
class AwardListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Award
        fields = ['id', 'name', 'description', 'logo', 'price']