from rest_framework import serializers
from group.models import Group, Category
from image.models import Image
from activity.models import Activity
from django.contrib.auth import get_user_model
User = get_user_model()
from base_serializers import UserSerializer, GroupSerializer, ImageSerializer, CategorySerializer

class ActivitySerializer(serializers.ModelSerializer):
    sender = UserSerializer()
    class Meta:
        model = Activity
        fields = ['id', 'sender', 'reciever', 'group', 'target', 'target_type', 'verb', 'post', 'created_at', 'updated_at']
        
class ActivityNotificationsSerializer(serializers.ModelSerializer):
    sender = UserSerializer()
    group = GroupSerializer()
    class Meta:
        model = Activity
        fields = ['id', 'sender', 'reciever', 'group', 'target', 'target_type', 'verb', 'done', 'post', 'created_at', 'updated_at']