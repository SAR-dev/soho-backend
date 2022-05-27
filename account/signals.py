from django.db.models.signals import post_save
from django.dispatch import receiver
from group.models import Group
from advertisement.models import Advertisement
from profiles.models import Profile
from reward.models import Reward
from django.contrib.auth import get_user_model
User = get_user_model()


@receiver(post_save, sender=User)
def create_related_profile(sender, instance, created, *args, **kwargs):
    if instance and created:
        instance.profile = Profile.objects.create(user=instance)
        instance.reward = Reward.objects.create(author=instance)
        instance.group = Group.objects.create(author=instance)
        instance.advertisement = Advertisement.objects.create(author=instance)
