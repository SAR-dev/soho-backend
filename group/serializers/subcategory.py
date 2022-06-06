from base_serializers import SubCategorySerializer, UserSerializer, ProfileSerializer, GroupSerializer, ImageSerializer, CategorySerializer
from rest_framework import serializers
from group.models import SubCategory, Category
from image.models import Image
from django.contrib.auth import get_user_model
User = get_user_model()


class GroupSubCategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['id', 'name', 'slug']
        read_only_fields = ['slug']