from rest_framework import serializers
from group.models import Group, Category
from image.models import Image
from django.contrib.auth import get_user_model
User = get_user_model()
from base_serializers import UserSerializer, ProfileSerializer, GroupSerializer, ImageSerializer, CategorySerializer


class GroupCategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'color', 'name', 'slug', 'about']
        read_only_fields = ['slug']


class GroupCategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'color', 'name', 'slug', 'about']


class GroupCategoryReriveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'color', 'name', 'slug', 'about']


class GroupCategoryUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'color', 'name', 'slug', 'about']
        read_only_fields = ['slug']
