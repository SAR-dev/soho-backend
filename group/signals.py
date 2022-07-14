from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Group
# from reward.models import Reward
from activity.models import Activity
from django.contrib.auth import get_user_model
User = get_user_model()


# @receiver(m2m_changed, sender=Group.subscribers.through)
# def add_subscriber_reward(sender, instance, action, pk_set, *args, **kwargs):
#     num_of_subscribers = instance.subscribers_count
#     if (num_of_subscribers):
#         reward = Reward.objects.select_related('author').get(author__username=instance.author.username)
#         if reward.subscribers:
#             reward.subscribers[str(instance.id)] = int(num_of_subscribers)
#         else:
#             reward.subscribers = {str(instance.id) : int(num_of_subscribers)}
#         reward.save()

