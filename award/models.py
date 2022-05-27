from django.db import models
from image.models import Image
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
User = get_user_model()


class Award(models.Model):
    class FreeAward(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(price=0)
        
    class PaidAward(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(price__gt=0)

    author = models.ForeignKey(
        User, on_delete=models.CASCADE, default=None, blank=True, null=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    logo = models.TextField(validators=[
        RegexValidator(
            regex='(<svg)([^<]*|[^>]*)',
            message="Invalid SVG code format!",
        ),
    ])
    price = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(100)])
    public = models.BooleanField(default=False)

    objects = models.Manager()
    free = FreeAward()
    paid = PaidAward()

    def __str__(self):
        return str(self.name)
