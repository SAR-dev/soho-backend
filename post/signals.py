from django.db.models.signals import post_save
from django.dispatch import receiver
from post.models import Post
from activity.models import Activity
from reward.models import Reward
from django.contrib.auth import get_user_model
User = get_user_model()


@receiver(post_save, sender=Post)
def add_post_reward_and_add_activity(sender, instance, created, *args, **kwargs):
    if instance and created:
        # post created
        Activity.objects.create(target=instance.id, group_id=instance.group.id,
                                sender_id=instance.author.id, target_type="post", verb="created")
        
    num_of_upvotes = instance.votes.count_up()
    if (num_of_upvotes % 10 == 0):
        reward = Reward.objects.select_related('author').get(
            author__id=instance.author.id
        )
        if reward.posts:
            reward.posts[str(instance.id)] = int(num_of_upvotes // 10)
        else:
            reward.posts = {str(instance.id): int(num_of_upvotes // 10)}
        reward.save()
