from rest_framework import serializers
from .models import Profile
from group.models import Group
from image.models import Image
from django.contrib.auth import get_user_model
User = get_user_model()
from base_serializers import UserSerializer, ProfileSerializer, GroupSerializer, ImageSerializer, CategorySerializer
        
class ProfileListSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Profile
        fields = ['id', 'bio', 'nickname', 'date_of_birth', 'email_address', 'phone_number', 'website', 'blood_group', 'user']
        
class ProfileRetriveSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Profile
        fields = ['id', 'bio', 'nickname', 'date_of_birth', 'email_address', 'phone_number', 'website', 'blood_group', 'user']

class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'bio', 'nickname', 'date_of_birth', 'email_address', 'phone_number', 'website', 'blood_group']
        
class ProfileImagesSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    thumbnail = serializers.SerializerMethodField()
    
    def get_thumbnail(self, obj):
        return obj.thumbnail.url
    
    class Meta:
        model = Image
        fields = ['id', 'image', 'thumbnail', 'height', 'width', 'author']
        read_only_fields = ['thumbnail']

