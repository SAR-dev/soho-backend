from django.db.models.signals import post_save
from django.dispatch import receiver
from group.models import Group, Category
from advertisement.models import Advertisement
from django.contrib.auth import get_user_model
User = get_user_model()


@receiver(post_save, sender=User)
def create_related(sender, instance, created, *args, **kwargs):
    if instance and created:
        instance.group = Group.objects.create(author=instance, rules={})
        instance.category = Category.objects.create(name="default", group=instance.group)
        instance.advertisement = Advertisement.objects.create(author=instance)
