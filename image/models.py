from django.db import models
from imagekit.models import ProcessedImageField, ImageSpecField
from imagekit.processors import ResizeToFit
import os
from uuid import uuid4
from django.utils.deconstruct import deconstructible
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


rename_and_relocate_post_image = RenameAndRelocateImage("images/post/")


class Image(models.Model):
    image = ProcessedImageField(upload_to=rename_and_relocate_post_image,
                                processors=[ResizeToFit(width=1400)],
                                format='JPEG',
                                options={'quality': 80},
                                height_field='height',
                                width_field='width')
    height = models.IntegerField(blank=True)
    width = models.IntegerField(blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, default=None, blank=True, null=True)

    objects = models.Manager()

    def __str__(self):
        return str(self.image)
