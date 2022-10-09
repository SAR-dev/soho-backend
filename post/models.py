from uuid import uuid4
import os
from django.utils.deconstruct import deconstructible
from imagekit.processors import ResizeToFit
from imagekit.models import ProcessedImageField
from django.db import models
from award.models import Award
from group.models import Group, Category, SubCategory
from image.models import Image
from choice.models import Choice
from vote.models import VoteModel
from django.core.validators import RegexValidator
from django.contrib.auth import get_user_model
from django.utils.timezone import now
User = get_user_model()


@deconstructible
class RenameAndRelocateImage(object):
    def __init__(self, sub_path):
        self.path = sub_path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        filename = '{}.{}'.format(uuid4().hex, ext)
        return os.path.join(self.path, filename)


rename_and_relocate_premier = RenameAndRelocateImage("images/premier/")


class Post(models.Model):
    class PostPublished(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status='published')

    class PostDraft(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status='draft')

    class PostCanVote(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status='published', can_vote=True)
    
    class PostCanComment(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status='published', can_comment=True)
        
    class PostCanBookmark(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status='published', release_time__isnull = False)

    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    TYPE_CHOICES = (
        ('discussion', 'Discussion'),
        ('premier', 'Premier'),
        ('ama', 'AMA'),
        ('poll', 'Poll'),
        ('announcement', 'Announcement'),
        ('drop', 'Drop'),
    )

    content = models.TextField(default=None, blank=True, null=True)
    images = models.ManyToManyField(
        Image, related_name='images', default=None, blank=True)
    choices = models.ManyToManyField(
        Choice, related_name='choices', default=None, blank=True)
    category = models.ForeignKey(
        Category, related_name="category", on_delete=models.SET_NULL, default=None, blank=True, null=True)
    sub_category = models.ForeignKey(
        SubCategory, related_name="sub_category", on_delete=models.CASCADE, default=None, blank=True, null=True)
    release_time = models.DateTimeField(null=True)
    duration = models.DurationField(null=True)
    thumbnail = models.ForeignKey(
        Image, related_name='thumbnail', on_delete=models.SET_NULL, default=None, blank=True, null=True)
    link = models.URLField(default=None, blank=True, null=True)
    
    is_blur = models.BooleanField(default=False)
    post_type = models.CharField(
        max_length=20, choices=TYPE_CHOICES, default='discussion')
    pinned_comment = models.IntegerField(default=None, blank=True, null=True)

    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='published')
    can_vote = models.BooleanField(default=True)
    can_comment = models.BooleanField(default=True)

    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='author')
    group = models.ForeignKey(
        Group, on_delete=models.CASCADE, default=None, blank=True, null=True)

    bookmarks = models.ManyToManyField(
        User, related_name='bookmarks', default=None, blank=True)
    claps = models.ManyToManyField(
        User, related_name='claps', default=None, blank=True, through='PostClaps')
    awards = models.ManyToManyField(
        Award, related_name='awards', default=None, blank=True, through='PostAwards')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    published = PostPublished()
    draft = PostDraft()
    canvote = PostCanVote()
    cancomment = PostCanComment()
    canbookmark = PostCanBookmark()

    class Meta:
        ordering = ('-id',)
        
    @property
    def bookmarks_count(self):
        return self.bookmarks.count()
    
    @property
    def num_vote_up(self):
        return self.claps.count()

    def __str__(self):
        return str(self.author)

class PostClaps(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class PostAwards(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    award = models.ForeignKey(Award, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)