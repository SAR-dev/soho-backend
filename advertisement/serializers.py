from rest_framework import serializers
from .models import Advertisement
from django.contrib.auth import get_user_model
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','is_active', 'username', 'first_name', 'last_name', 'is_active', 'avatar']

class AdvertisementRetriveSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    class Meta:
        model = Advertisement
        fields = ['id','is_active', 'author', 'image', 'source', 'link']

class AdvertisementUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertisement
        fields = ['is_active', 'image', 'source', 'link']