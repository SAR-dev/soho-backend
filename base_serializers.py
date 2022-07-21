from rest_framework import serializers
from post.models import Post
from moderator.models import Moderator
from award.models import Award
from comment.models import Comment
from group.models import Group, Category, SubCategory
from image.models import Image
from choice.models import Choice
from django.contrib.auth import get_user_model
User = get_user_model()
from django.db.models import Q


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name',
                  'last_name', 'is_active', 'avatar']


class GroupSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    is_admin = serializers.SerializerMethodField()
    is_moderator = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = ['id', 'slogan', 'members_name', 'color',  'status', 'title', 'author', 'is_admin', 'is_moderator', 'created_at', 'updated_at']
        
    def get_is_admin(self, obj):
        return obj.author == self.context.get('request').user
    
    def get_is_moderator(self, obj):
        return Moderator.verified.filter(moderator = self.context.get('request').user, admin = obj.author).exists()


class CategorySerializer(serializers.ModelSerializer):
    group = GroupSerializer()

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'group']
        
class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['id', 'name', 'slug', 'emoji']
        
class AwardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Award
        fields = ['id', 'name', 'logo', 'description', 'price']

class PostCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']
        
class PostGroupSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    subscribers_count = serializers.ReadOnlyField()
    subscribed = serializers.SerializerMethodField()
    post_count = serializers.SerializerMethodField()
    is_admin = serializers.SerializerMethodField()
    is_moderator = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = ['id', 'status', 'author', 'members_name', 'subscribers_count', 'subscribed', 'post_count', 'is_admin', 'is_moderator']

    def get_post_count(self, obj):
        return Post.published.filter(group=obj).count()

    def get_subscribed(self, obj):
        return obj.subscribers.filter(pk=self.context.get('request').user.id).exists()
    
    def get_is_admin(self, obj):
        return obj.author == self.context.get('request').user
    
    def get_is_moderator(self, obj):
        return Moderator.verified.filter(moderator = self.context.get('request').user, admin = obj.author).exists()


class ImageSerializer(serializers.ModelSerializer):
    author = UserSerializer()

    class Meta:
        model = Image
        fields = ['id', 'image', 'height', 'width', 'description', 'author']
        
class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['id', 'text', 'num_vote_up']
        
        
class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    images = ImageSerializer(many=True)
    choices = ChoiceSerializer(many=True)
    category = PostCategorySerializer()
    group = PostGroupSerializer()
    thumbnail = ImageSerializer()
    bookmarks_count = serializers.ReadOnlyField()
    bookmarked = serializers.SerializerMethodField()
    upvoted = serializers.SerializerMethodField()
    release_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M")
    choices_voted = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    available_awards = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'status', 'content', 'images', 'link', 'category', 'release_time', 'thumbnail', 'is_blur', 'post_type', 'pinned_comment',
                  'can_vote', 'can_comment', 'author', 'group', 'choices', 'choices_voted', 'num_vote_up', 'bookmarks_count', 'bookmarked', 'upvoted', 'comments_count', 'available_awards', 'awards', 'created_at', 'updated_at']

    def get_bookmarked(self, obj):
        return obj.bookmarks.filter(pk=self.context.get('request').user.id).exists()

    def get_upvoted(self, obj):
        return obj.votes.exists_up(self.context.get('request').user.id)

    def get_choices_voted(self, obj):
        voted = False
        for item in obj.choices.all():
            if item.votes.exists_up(self.context.get('request').user.id):
                voted = item.id
        return voted

    def get_comments_count(self, obj):
        return Comment.objects.filter(post=obj.id).count()
    
    def get_available_awards(self, obj):
        objects = AwardSerializer(data = Award.objects.filter(Q(author_id=obj.group.author.id) | Q(public=True)) , many=True)
        objects.is_valid()
        return objects.data
    
class CommentSerializer(serializers.ModelSerializer):
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