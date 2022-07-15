from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Comment
from activity.models import Activity
from django.contrib.auth import get_user_model
User = get_user_model()


@receiver(post_save, sender=Comment)
def add_add_activity(sender, instance, created, *args, **kwargs):
    if instance and created:
        # comment created
        Activity.objects.create(target=instance.id, post=instance.post.id, group_id=instance.post.group.id,
                                sender_id=instance.author.id, target_type="comment", reciever_id=instance.post.author.id, verb="commented")
        # reply created
        if instance.parent:
            Activity.objects.create(target=instance.id, post=instance.post.id, group_id=instance.post.group.id,
                                    sender_id=instance.author.id, target_type="comment", reciever_id=instance.parent.author.id, verb="replied")
        # mentioned
        if instance.mention:
            Activity.objects.create(target=instance.id, post=instance.post.id, group_id=instance.post.group.id,
                                    sender_id=instance.author.id, target_type="comment", reciever_id=instance.mention.id, verb="mentioned")

