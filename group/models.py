from tokenize import group
from unicodedata import category
from django.db import models
from django.core.validators import RegexValidator
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit
from utils.generators import generate_unique_slug
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save, pre_delete
from django.utils.deconstruct import deconstructible
import os
from uuid import uuid4
from image.models import Image
from nanoid import generate
from django.contrib.auth import get_user_model
User = get_user_model()

@deconstructible
class RenameAndRelocateImage(object):
    def __init__(self, sub_path):
        self.path = sub_path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        filename = '{}.{}'.format(uuid4().hex, ext)
        return os.path.join(self.path, filename)
rename_and_relocate_cover = RenameAndRelocateImage("images/group/cover/")

class Group(models.Model):
    class PublicGroup(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status='public')
    
    class PrivateGroup(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status='private')
        
    STATUS_CHOICES = (
        ('public', 'Public'),
        ('private', 'Private'),
    )
    
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    
    title = models.CharField(max_length=50, null=True, blank=True)
    slogan = models.CharField(max_length=30, null=True, blank=True)
    rules = models.TextField(default=None, blank=True, null=True)
    members_name = models.CharField(max_length=10, default="Members")
    color = models.CharField(max_length=100, default="#6B46C1", validators=[
        RegexValidator(
            regex='^#[0-9a-fA-F]{6}$',
            message="Invalid color format. RGB hex color format needed.",
        ),
    ])
    token = models.TextField(max_length=20 ,null=True, blank=True, unique=True, validators=[
        RegexValidator(
            regex='^([A-Z0-9]{10})$',
            message="Invalid token format! Token should be alphanumeric of 10 digit.",
        ),
    ])
    cover = ProcessedImageField(upload_to=rename_and_relocate_cover,
                                 default='images/cover.jpg',
                                 processors=[ResizeToFit(width=1400)],
                                 format='JPEG',
                                 options={'quality': 60})
    subscribers = models.ManyToManyField(User, related_name='subscribers', default=None, blank=True)
    blacklists = models.ManyToManyField(User, related_name='blacklists', default=None, blank=True)
    moderators = models.ManyToManyField(User, related_name='moderators', default=None, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='public')

    objects = models.Manager()
    public = PublicGroup()
    private = PrivateGroup()
    
    @property
    def subscribers_count(self):
        return self.subscribers.count()

    def __str__(self):
        return str(self.author)
    
    class Meta:
        ordering = ['-id']

@receiver(pre_save, sender=Group)
def token_generator(sender, instance, *args, **kwargs):
    unique_token = generate('123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ', 10)
    # Generate token untill it is unique
    while Group.objects.filter(token=unique_token).exclude(id=instance.id).exists():
        unique_token = generate('123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ', 10)
    instance.token = unique_token
        
@receiver(post_save, sender=Group)
def add_author_to_subscribers(sender, instance, *args, **kwargs):
    subscribers = Group.objects.get(id=instance.id).subscribers
    subscribers.add(instance.author.id)
    
class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=50 ,unique=True, validators=[
        RegexValidator(
            regex='^[a-z0-9_-]{3,50}$',
            message="Invalid slug format! Slug should be between 3-50 characters. Use hyphen '-' or underscore '_' between letters if needed. ",
        ),
    ])
    emoji = models.CharField(max_length=500, default="")
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='group', default=None, blank=True, null=True)
    
    objects = models.Manager()
    
    def __str__(self):
        return str(self.name)
    
    class Meta:
        verbose_name_plural = "categories"
        ordering = ['-id']
        
@receiver(pre_save, sender=Category)
def unique_slug(sender, instance, *args, **kwargs):
    if len(instance.slug) == 0:
        instance.slug = generate_unique_slug(Category, instance.name)

@receiver(pre_delete, sender=Category)
def set_default_category_for_subcategory(sender, instance, *args, **kwargs):
    cat = Category.objects.get(name = 'default', group__id = instance.group.id)
    SubCategory.objects.filter(category = instance).update(category_id = cat.id)
        
class SubCategory(models.Model):
    name = models.CharField(max_length=100)
    emoji = models.CharField(max_length=500, default="")
    slug = models.SlugField(max_length=50 ,unique=True, validators=[
        RegexValidator(
            regex='^[a-z0-9_-]{3,50}$',
            message="Invalid slug format! Slug should be between 3-50 characters. Use hyphen '-' or underscore '_' between letters if needed. ",
        ),
    ])
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, related_name='parent_category', default=None, blank=True, null=True)
    
    objects = models.Manager()
    
    def __str__(self):
        return str(self.name)
    
    class Meta:
        verbose_name_plural = "sub-categories"
        ordering = ['-id']
        
@receiver(pre_save, sender=SubCategory)
def unique_slug(sender, instance, *args, **kwargs):
    if len(instance.slug) == 0:
        instance.slug = generate_unique_slug(SubCategory, instance.name)