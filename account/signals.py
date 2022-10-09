from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Account
from group.models import Group, Category, SubCategory
from advertisement.models import Advertisement
from django.contrib.auth import get_user_model
User = get_user_model()


@receiver(post_save, sender=User)
def create_related(sender, instance, created, *args, **kwargs):
    if instance and created:
        instance.group = Group.objects.create(author=instance, rules="")
        instance.category = Category.objects.create(name="default", group=instance.group)
        category = Category.objects.create(name="General", group=instance.group)
        instance.subcategory = SubCategory.objects.create(name="General", category=category, emoji="😺")
        instance.advertisement = Advertisement.objects.create(author=instance)


@receiver(pre_save, sender=Account)
def save(sender, instance, *args, **kwargs):
    # Replace avatar
    if instance.avatar:
        try:
            acc = Account.objects.get(id=instance.id)
            pre = acc.avatar
            post = instance.avatar
            if (pre != post and pre != "images/avatar.jpg"):
                pre.delete(save=True)
        except:
            pass