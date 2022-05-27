from rest_framework import serializers
from .models import Moderator
from django.contrib.auth import get_user_model
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username', 'first_name', 'last_name', 'is_active', 'avatar']
        
class ModeratorListSerializer(serializers.ModelSerializer):
    admin = UserSerializer()
    moderator = UserSerializer()
    class Meta:
        model = Moderator
        fields = ['id', 'color', 'admin', 'moderator', 'is_verified', 'nickname']
        
class ModeratorCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Moderator
        fields = ['nickname']
        
class ModeratorRetriveSerializer(serializers.ModelSerializer):
    admin = UserSerializer()
    moderator = UserSerializer()
    class Meta:
        model = Moderator
        fields = ['id', 'color', 'admin', 'moderator', 'is_verified', 'nickname']
        
class ModeratorAdminUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Moderator
        fields = [ 'color','nickname']
        
class ModeratorSelfUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Moderator
        fields = ['is_verified']