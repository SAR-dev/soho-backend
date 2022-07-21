from base_serializers import SubCategorySerializer, UserSerializer, GroupSerializer, ImageSerializer, CategorySerializer, ChoiceSerializer, PostSerializer, PostGroupSerializer
from rest_framework import serializers
from post.models import Post, PostAwards
from moderator.models import Moderator
from award.models import Award
from comment.models import Comment
from group.models import Group, Category
from image.models import Image
from utils.truncate import truncate_html_words
from django.contrib.auth import get_user_model
User = get_user_model()
from django.db.models import Q
from utils.get_seconds import get_seconds

class AwardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Award
        fields = ['id', 'name', 'logo', 'description', 'price']

class PostAwardSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostAwards
        fields = ['author', 'post', 'award']

class PostCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']


class DiscussionPostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'content', 'images', 'category', 'sub_category', 'link', 'status']

    def validate(self, data):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user

        if(len(data['content']) < 20):
            raise serializers.ValidationError(
                {"content": "Text content is too short!"})
        for x in data['images']:
            if(x.author != user):
                raise serializers.ValidationError(
                    {"images": "Select images that you uploaded only"})
        data['release_time'] = None
        data['thumbnail'] = None
        return data


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'content', 'images', 'link', 'category', 'sub_category', 'release_time', 'duration',
                  'thumbnail', 'post_type', 'can_vote', 'can_comment', 'choices', 'status']

    def validate(self, data):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user

        if(data['post_type'] == 'discussion'):
            if(len(data['content']) < 10):
                raise serializers.ValidationError(
                    {"content": "Text content is too short!"})
            for x in data['images']:
                if(x.author != user):
                    raise serializers.ValidationError(
                        {"images": "Select images that you uploaded only"})
            data['release_time'] = None
            data['duration'] = None
            data['thumbnail'] = None
            data['choices'] = ''

        elif(data['post_type'] == 'announcement'):
            if(len(data['content']) < 10):
                raise serializers.ValidationError(
                    {"content": "Text content is too short!"})
            for x in data['images']:
                if(x.author != user):
                    raise serializers.ValidationError(
                        {"images": "Select images that you uploaded only"})
            data['release_time'] = None
            data['duration'] = None
            data['thumbnail'] = None
            data['choices'] = ''

        elif(data['post_type'] == 'premier'):
            print(data)
            if(data['thumbnail'] is None):
                raise serializers.ValidationError(
                    {"thumbnail": "Thumbnail is required for this type of post!"})
            if(data['release_time'] is None):
                raise serializers.ValidationError(
                    {"release_time": "Release time is required for this type of post!"})
            # if(len(data['link']) < 4):
            #     raise serializers.ValidationError(
            #         {"link": "Premier link in required!"})
            data['duration'] = None
            data['content'] = ''
            data['images'] = ''
            data['choices'] = ''
            data['category'] = None

        elif(data['post_type'] == 'ama'):
            if(len(data['content']) < 10):
                raise serializers.ValidationError(
                    {"content": "Text content is too short!"})
            if(data['release_time'] is None):
                raise serializers.ValidationError(
                    {"release_time": "Release time is required for this type of post!"})
            if(data['duration'] is None):
                raise serializers.ValidationError(
                    {"duration": "Duration is required for this type of post!"})
            if(get_seconds(data['duration']) < 3600):
                raise serializers.ValidationError(
                    {"duration": "Duration must be at least 1 hour!"})
            data['thumbnail'] = None
            data['images'] = ''
            data['choices'] = ''
            data['category'] = None
            data['link'] = None

        elif(data['post_type'] == 'poll'):
            if(len(data['content']) < 10):
                raise serializers.ValidationError(
                    {"content": "Text content is too short!"})
            for x in data['choices']:
                if(x.author != user):
                    raise serializers.ValidationError(
                        {"choices": "Select choices that you created only"})
            if(data['duration'] is None):
                raise serializers.ValidationError(
                    {"duration": "Duration is required for this type of post!"})
            if(get_seconds(data['duration']) < 3600):
                raise serializers.ValidationError(
                    {"duration": "Duration must be at least 1 hour!"})
            data['thumbnail'] = None
            data['images'] = ''
            data['category'] = None
            data['release_time'] = None
            data['link'] = None

        return data


class PostListSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    images = ImageSerializer(many=True)
    choices = ChoiceSerializer(many=True)
    awards = PostAwardSerializer(many=True)
    category = PostCategorySerializer()
    sub_category = SubCategorySerializer()
    group = PostGroupSerializer()
    thumbnail = ImageSerializer()
    bookmarks_count = serializers.ReadOnlyField()
    bookmarked = serializers.SerializerMethodField()
    content = serializers.SerializerMethodField()
    upvoted = serializers.SerializerMethodField()
    release_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M")
    choices_voted = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    available_awards = serializers.SerializerMethodField()
    awards = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'status', 'content', 'images', 'link', 'category', 'sub_category', 'release_time',  'duration','thumbnail', 'is_blur', 'post_type',
                  'can_vote', 'can_comment', 'author', 'group', 'choices', 'choices_voted', 'num_vote_up', 'bookmarks_count', 'bookmarked', 'upvoted', 'comments_count', 'available_awards', 'awards', 'created_at', 'updated_at']

    def get_content(self, obj):
        if (obj.post_type == "announcement"):
            return obj.content
        else:
            return truncate_html_words(obj.content, 80)

    def get_bookmarked(self, obj):
        return obj.bookmarks.filter(pk=self.context.get('request').user.id).exists()

    def get_upvoted(self, obj):
        return self.context.get('request').user in obj.claps.all()
        # return obj.votes.exists_up(self.context.get('request').user.id)

    def get_choices_voted(self, obj):
        voted = False
        for item in obj.choices.all():
            if item.votes.exists_up(self.context.get('request').user.id):
                voted = item.id
        return voted

    def get_comments_count(self, obj):
        return Comment.objects.filter(post=obj.id).count()
    
    def get_awards(self, obj):
        objects = PostAwardSerializer(data = PostAwards.objects.filter(author = self.context.get('request').user.id, post=obj.id) , many=True)
        objects.is_valid()
        return objects.data

    def get_available_awards(self, obj):
        objects = AwardSerializer(data = Award.objects.filter(Q(author_id=obj.group.author.id) | Q(public=True)) , many=True)
        objects.is_valid()
        return objects.data


class PostReriveSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    images = ImageSerializer(many=True)
    choices = ChoiceSerializer(many=True)
    category = PostCategorySerializer()
    # awards = PostAwardSerializer(many=True)
    sub_category = SubCategorySerializer()
    group = PostGroupSerializer()
    thumbnail = ImageSerializer()
    bookmarks_count = serializers.ReadOnlyField()
    bookmarked = serializers.SerializerMethodField()
    upvoted = serializers.SerializerMethodField()
    release_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M")
    choices_voted = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    available_awards = serializers.SerializerMethodField()
    awards = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'status', 'content', 'images', 'link', 'category', 'sub_category', 'release_time',  'duration','thumbnail', 'is_blur', 'post_type', 'pinned_comment',
                  'can_vote', 'can_comment', 'author', 'group', 'choices', 'choices_voted', 'num_vote_up', 'bookmarks_count', 'bookmarked', 'upvoted', 'comments_count', 'available_awards', 'awards', 'created_at', 'updated_at']

    def get_bookmarked(self, obj):
        return obj.bookmarks.filter(pk=self.context.get('request').user.id).exists()

    def get_upvoted(self, obj):
        return self.context.get('request').user in obj.claps.all()

    def get_choices_voted(self, obj):
        voted = False
        for item in obj.choices.all():
            if item.votes.exists_up(self.context.get('request').user.id):
                voted = item.id
        return voted

    def get_comments_count(self, obj):
        return Comment.objects.filter(post=obj.id).count()
    
    def get_awards(self, obj):
        objects = PostAwardSerializer(data = PostAwards.objects.filter(author = self.context.get('request').user.id, post=obj.id) , many=True)
        objects.is_valid()
        return objects.data

    def get_available_awards(self, obj):
        objects = AwardSerializer(data = Award.objects.filter(Q(author_id=obj.group.author.id) | Q(public=True)) , many=True)
        objects.is_valid()
        return objects.data


class PostUpdateSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    class Meta:
        model = Post
        fields = ['id', 'content', 'images', 'link', 'category', 'sub_category', 'release_time', 'duration',
                  'thumbnail', 'is_blur', 'post_type', 'can_vote', 'can_comment', 'choices', 'author', 'images']

    def validate(self, data):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user

        if(data['post_type'] == 'discussion'):
            if(len(data['content']) < 10):
                raise serializers.ValidationError(
                    {"content": "Text content is too short!"})
            for x in data['images']:
                if(x.author != user):
                    raise serializers.ValidationError(
                        {"images": "Select images that you uploaded only"})
            data['release_time'] = None
            data['duration'] = None
            data['thumbnail'] = None
            data['choices'] = ''

        elif(data['post_type'] == 'announcement'):
            if(len(data['content']) < 10):
                raise serializers.ValidationError(
                    {"content": "Text content is too short!"})
            for x in data['images']:
                if(x.author != user):
                    raise serializers.ValidationError(
                        {"images": "Select images that you uploaded only"})
            data['release_time'] = None
            data['duration'] = None
            data['thumbnail'] = None
            data['choices'] = ''

        elif(data['post_type'] == 'premier'):
            if(data['thumbnail'] is None):
                raise serializers.ValidationError(
                    {"thumbnail": "Thumbnail is required for this type of post!"})
            if(data['release_time'] is None):
                raise serializers.ValidationError(
                    {"release_time": "Release time is required for this type of post!"})
            # if(len(data['link']) < 4):
            #     raise serializers.ValidationError(
            #         {"link": "Premier link in required!"})
            data['duration'] = None
            data['content'] = ''
            data['images'] = ''
            data['choices'] = ''
            data['category'] = None

        elif(data['post_type'] == 'ama'):
            if(len(data['content']) < 10):
                raise serializers.ValidationError(
                    {"content": "Text content is too short!"})
            if(data['release_time'] is None):
                raise serializers.ValidationError(
                    {"release_time": "Release time is required for this type of post!"})
            if(data['duration'] is None):
                raise serializers.ValidationError(
                    {"duration": "Duration is required for this type of post!"})
            if(get_seconds(data['duration']) < 3600):
                raise serializers.ValidationError(
                    {"duration": "Duration must be at least 1 hour!"})
            data['thumbnail'] = None
            data['images'] = ''
            data['choices'] = ''
            data['category'] = None
            data['link'] = None

        elif(data['post_type'] == 'poll'):
            if(len(data['content']) < 10):
                raise serializers.ValidationError(
                    {"content": "Text content is too short!"})
            for x in data['choices']:
                if(x.author != user):
                    raise serializers.ValidationError(
                        {"choices": "Select choices that you created only"})
            if(data['duration'] is None):
                raise serializers.ValidationError(
                    {"duration": "Duration is required for this type of post!"})
            if(get_seconds(data['duration']) < 3600):
                raise serializers.ValidationError(
                    {"duration": "Duration must be at least 1 hour!"})
            data['thumbnail'] = None
            data['images'] = ''
            data['category'] = None
            data['release_time'] = None
            data['link'] = None

        return data

class PostBookmarksSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    group = PostGroupSerializer()
    release_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M")

    class Meta:
        model = Post
        fields = ['id', 'release_time', 'author', 'group','created_at']