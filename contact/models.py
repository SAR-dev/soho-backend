from django.db import models
from group.models import Group
from django.db.models import Q
from django.contrib.auth import get_user_model
User = get_user_model()

class Contact(models.Model):  
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, default=None, blank=True, null=True)
    details = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = models.Manager()
    
    class Meta:
        ordering = ('-id',)
        
    def __str__(self):
        return str(self.details)