from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()


class Reward(models.Model):
    posts = models.JSONField(default=dict)
    comments = models.JSONField(default=dict)
    subscribers = models.JSONField(default=dict)
    extra = models.JSONField(default=dict)

    author = models.OneToOneField(User, on_delete=models.CASCADE)

    objects = models.Manager()

    def __str__(self):
        return str(self.author)

    @property
    def total_score(self):
        score = "{:.2f}".format(sum(self.extra.values()) + pow(sum(self.posts.values()), 1.25) + pow(sum(self.comments.values()), 0.85) + pow(sum(self.subscribers.values()), 0.65))
        return score

    class Meta:
        ordering=['-id']
