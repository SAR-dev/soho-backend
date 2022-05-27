from django.db import models
from group.models import Group, Category
from django.db.models import Q
from django.contrib.auth import get_user_model
User = get_user_model()

class Activity(models.Model):
    class Read(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(done=True)
    class Unread(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(done=False)
        
    TARGET_TYPES = (
        ('post', 'Post'),
        ('comment', 'Comment'),
        ('user', 'User'),
    )
    
    VERB_TYPES = (
        ('created', 'Created'),
        ('clapped', 'Clapped'),
        ('awarded', 'Awarded'),
        ('commented', 'Commented'),
        ('replied', 'Replied'),
        ('mentioned', 'Mentioned'),
        ('joined', 'Joined'),
    )
    
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='sender')
    reciever = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reciever', default=None, blank=True, null=True)
    group = models.ForeignKey(
        Group, on_delete=models.CASCADE, default=None, blank=True, null=True)
    post = models.IntegerField(default=0)
    target = models.IntegerField()
    target_type = models.CharField(
        max_length=10, choices=TARGET_TYPES, default='post')
    verb = models.CharField(
        max_length=10, choices=VERB_TYPES, default='created')
    done = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = models.Manager()
    read = Read()
    unread = Unread()
    
    class Meta:
        ordering = ('-id',)
        verbose_name_plural = "activities"
        
    def __str__(self):
        return str(self.sender)