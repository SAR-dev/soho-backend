from rest_framework import serializers
from .models import Image
from django.contrib.auth import get_user_model
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username', 'first_name', 'last_name', 'is_active', 'avatar']
        
class ImageSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    class Meta:
        model = Image
        fields = ['id', 'image', 'height', 'width', 'author']
        
class ImageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'image', 'description']
        
class ImageRetriveSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    class Meta:
        model = Image
        fields = ['id', 'image', 'height', 'width', 'author']
        
class ImageUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'description']