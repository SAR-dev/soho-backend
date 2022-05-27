from base_serializers import UserSerializer, ProfileSerializer, GroupSerializer, ImageSerializer, CategorySerializer, ChoiceSerializer, PostSerializer
from rest_framework import serializers
from .models import Comment
import re
        
class CommentListSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    mention = UserSerializer()
    hands_count = serializers.ReadOnlyField()
    upvoted = serializers.SerializerMethodField()
    hands_raised = serializers.SerializerMethodField()
    class Meta:
        model = Comment
        fields = ['id', 'is_active', 'content', 'mention', 'author', 'post', 'parent', 'upvoted', 'num_vote_up', 'hands_raised', 'hands_count', 'created_at']

    def get_upvoted(self, obj):
        return obj.votes.exists_up(self.context.get('request').user.id)

    def get_hands_raised(self, obj):
        return obj.hands.filter(pk=self.context.get('request').user.id).exists()
        
class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'is_active', 'content', 'mention', 'created_at']
        
    def validate(self, data):
        r = re.match(r'^(((<\w+>)+[ \n(<br>)]*(<\/\w+>)+)+)|<br>$', data['content'])
        if(r):
            raise serializers.ValidationError(
                {"content": "Content is too short!"})
        return data
        
class CommentChildCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'is_active', 'content', 'mention', 'author', 'post', 'created_at']
        read_only_fields = ['author', 'post']
        
    def validate(self, data):
        r = re.match(r'^(((<\w+>)+[ \n(<br>)]*(<\/\w+>)+)+)|<br>$', data['content'])
        if(r):
            raise serializers.ValidationError(
                {"content": "Content is too short!"})
        return data
        
class CommentRetriveSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    mention = UserSerializer()
    hands_count = serializers.ReadOnlyField()
    upvoted = serializers.SerializerMethodField()
    hands_raised = serializers.SerializerMethodField()
    class Meta:
        model = Comment
        fields = ['id', 'is_active', 'content', 'mention', 'author', 'post', 'parent', 'upvoted', 'num_vote_up', 'hands_raised', 'hands_count', 'created_at']

    def get_upvoted(self, obj):
        return obj.votes.exists_up(self.context.get('request').user.id)

    def get_hands_raised(self, obj):
        return obj.hands.filter(pk=self.context.get('request').user.id).exists()
        
class CommentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'is_active', 'content', 'mention', 'created_at']
        
    def validate(self, data):
        r = re.match(r'^(((<\w+>)+[ \n(<br>)]*(<\/\w+>)+)+)|<br>$', data['content'])
        if(r):
            raise serializers.ValidationError(
                {"content": "Content is too short!"})
        return data
    
class CommentBanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['is_active', 'content']
        
    def validate(self, data):
        data['is_active'] = False
        if(len(data['content']) < 10):
            raise serializers.ValidationError(
                {"Message": "Message is too short!"})
            
        return data