from django.db.models.signals import post_save
from django.dispatch import receiver
from post.models import Post
from activity.models import Activity
from django.contrib.auth import get_user_model
User = get_user_model()


@receiver(post_save, sender=Post)
def add_activity(sender, instance, created, *args, **kwargs):
    if instance and created:
        # post created
        Activity.objects.create(target=instance.id, group_id=instance.group.id,
                                sender_id=instance.author.id, target_type="post", verb="created")
