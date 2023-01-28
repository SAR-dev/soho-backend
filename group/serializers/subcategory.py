from base_serializers import SubCategorySerializer, UserSerializer, GroupSerializer, ImageSerializer, CategorySerializer
from rest_framework import serializers
from group.models import SubCategory, Category
from image.models import Image
from django.contrib.auth import get_user_model
User = get_user_model()


class GroupSubCategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['id', 'name', 'slug', 'emoji']
        read_only_fields = ['slug']

        def validate(self, data):
            if(len(data['emoji']) < 1):
                raise serializers.ValidationError(
                        {"emoji": "Select a emoji"})

class ChangeParentCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['category']

class UpdateSubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['name', 'emoji', 'slug']