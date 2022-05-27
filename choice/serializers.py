from rest_framework import serializers
from .models import Choice
from django.contrib.auth import get_user_model
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username', 'first_name', 'last_name', 'is_active', 'avatar']
        
class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['id', 'text', 'num_vote_up']
        
class ChoiceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['id', 'text']
        
class ChoiceRetriveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['id', 'text', 'num_vote_up']
        
class ChoiceUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['id', 'text']