from django.db import models
from group.models import Group
from django.db.models import Q
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit
from django.utils.deconstruct import deconstructible
import os
from uuid import uuid4
from django.core.validators import RegexValidator
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
rename_and_relocate_advertisement = RenameAndRelocateImage("images/advertisement/")

class Advertisement(models.Model):  
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    image = ProcessedImageField(upload_to=rename_and_relocate_advertisement,
                                 default='images/advertisement.jpg',
                                 processors=[ResizeToFit(width=400)],
                                 format='JPEG',
                                 options={'quality': 60})
    source = models.TextField()
    link = models.URLField(default=None, blank=True, null=True)
    is_active = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = models.Manager()
    
    class Meta:
        ordering = ('-id',)
        
    def __str__(self):
        return str(self.author)