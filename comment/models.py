from django.db import models
from vote.models import VoteModel
from post.models import Post
from image.models import Image
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model
User = get_user_model()

class Comment(VoteModel, models.Model):
    class CommentActive(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(is_active=True)
        
    content = models.CharField(max_length=2000)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    author = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    mention = models.ForeignKey(User, related_name='mention', on_delete=models.DO_NOTHING, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    hands = models.ManyToManyField(User, related_name='hands', default=None, blank=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='childern')
    is_active = models.BooleanField(default=True)
    
    objects = models.Manager()
    active = CommentActive()
    
    class Meta:
        ordering =('-id',)
        
    def delete(self):
        comment = Comment.objects.filter(parent = self.pk)
        if comment.exists():
            self.is_active = False
            self.content = "This comment has been removed."
            self.save()
        else:
            super(Comment, self).delete()
            
    @property
    def hands_count(self):
        return self.hands.count()

    def __str__(self):
        return str(self.content)