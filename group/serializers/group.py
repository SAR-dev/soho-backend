from base_serializers import UserSerializer, ProfileSerializer, GroupSerializer, ImageSerializer, CategorySerializer
from rest_framework import serializers
from group.models import Group, Category
from moderator.models import Moderator
from activity.models import Activity
from post.models import Post
from award.models import Award
from rest_framework.renderers import JSONRenderer
from django.contrib.auth import get_user_model
User = get_user_model()

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'color', 'name', 'slug', 'about']

class AwardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Award
        fields = ['id', 'name', 'logo', 'description', 'price']

class GroupListSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    subscribers_count = serializers.ReadOnlyField()
    subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = ['id', 'title', 'slogan', 'members_name', 'color', 'status', 'subscribers_count',
                  'subscribed', 'author', 'created_at', 'updated_at']

    def get_subscribed(self, obj):
        return obj.subscribers.filter(pk=self.context.get('request').user.id).exists()


class GroupRetriveSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    subscribers_count = serializers.ReadOnlyField()
    subscribed = serializers.SerializerMethodField()
    post_count = serializers.SerializerMethodField()
    is_admin = serializers.SerializerMethodField()
    is_moderator = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = ['id', 'title', 'slogan', 'members_name', 'color',  'status', 'cover', 'subscribers_count',
                  'subscribed', 'post_count', 'author', 'is_admin', 'is_moderator', 'created_at', 'updated_at']

    def get_post_count(self, obj):
        return Post.published.filter(group=obj).count()

    def get_subscribed(self, obj):
        return obj.subscribers.filter(pk=self.context.get('request').user.id).exists()
    
    def get_is_admin(self, obj):
        return obj.author == self.context.get('request').user
    
    def get_is_moderator(self, obj):
        try:
            return Moderator.verified.filter(moderator = self.context.get('request').user, admin = obj.author).exists()
        except:
            return False
    
class GroupRulesRetriveSerializer(serializers.ModelSerializer):
    author = UserSerializer()

    class Meta:
        model = Group
        fields = ['id', 'rules', 'author', 'created_at', 'updated_at']


class GroupUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['slogan', 'members_name', 'color', 'title', 'status', 'token', 'rules']


class GroupSubscribersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name',
                  'last_name', 'is_active', 'avatar']


class GroupBlacklistsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name',
                  'last_name', 'is_active', 'avatar']
        
class GroupLeaderboardSerializer(serializers.ModelSerializer):
    reciever = UserSerializer()
    claps = serializers.SerializerMethodField()
    
    class Meta:
        model = Activity
        fields = ['reciever', 'claps']
    
    def get_claps(self, obj):
        return obj["claps"]
