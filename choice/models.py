from django.db import models
from vote.models import VoteModel
from django.contrib.auth import get_user_model
User = get_user_model()

class Choice(VoteModel, models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, default=None, blank=True, null=True)
    text = models.CharField(max_length=100)

    objects = models.Manager()

    def __str__(self):
        return str(self.text)