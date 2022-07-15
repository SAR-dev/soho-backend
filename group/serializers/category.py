from base_serializers import SubCategorySerializer, UserSerializer, GroupSerializer, ImageSerializer, CategorySerializer
from rest_framework import serializers
from group.models import SubCategory, Category
from image.models import Image
from django.contrib.auth import get_user_model
User = get_user_model()


class GroupCategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'color', 'name', 'slug', 'about', 'emoji']
        read_only_fields = ['slug']


class GroupCategoryListSerializer(serializers.ModelSerializer):
    sub_categories = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'color', 'name', 'slug', 'about', 'sub_categories', 'emoji']

    def get_sub_categories(self, obj):
        objects = SubCategorySerializer(data=SubCategory.objects.filter(category_id=obj.id), many=True)
        objects.is_valid()
        return objects.data


class GroupCategoryReriveSerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields=['id', 'color', 'name', 'slug', 'about', 'emoji']


class GroupCategoryUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields=['id', 'color', 'name', 'slug', 'about', 'emoji']
        read_only_fields=['slug']
