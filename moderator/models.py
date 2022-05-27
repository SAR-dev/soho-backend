from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth import get_user_model
User = get_user_model()

class Moderator(models.Model):
    class Verified(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(is_verified=True)
        
    class Unverified(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(is_verified=False)
        
    admin = models.ForeignKey(User, related_name='admin', on_delete=models.CASCADE)
    moderator = models.ForeignKey(User, related_name='moderator', on_delete=models.CASCADE)
    is_verified = models.BooleanField(default=False)
    nickname = models.CharField(null=True, blank=True, max_length=100)
    color = models.CharField(max_length=100, default="#d5b60a", validators=[
        RegexValidator(
            regex='^#[0-9a-fA-F]{6}$',
            message="Invalid color format. RGB hex color format needed.",
        ),
    ])
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    verified = Verified()
    unverified = Unverified()
    
    class Meta:
        ordering =('-id',)

    def __str__(self):
        return str(self.admin)