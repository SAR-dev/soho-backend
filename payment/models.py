from django.db import models
from group.models import Group
from django.db.models import Q
from django.contrib.auth import get_user_model
User = get_user_model()

class Payment(models.Model):  
    class PaymentCompleted(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(completed=True)

    checkout_id = models.CharField(max_length=250)
    payor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="payor", default=None, blank=True, null=True)
    payee = models.ForeignKey(User, on_delete=models.CASCADE, related_name="payee", default=None, blank=True, null=True)
    amount = models.IntegerField()
    currency = models.CharField(max_length=10)
    interval = models.CharField(max_length=10)
    completed = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = models.Manager()
    finished = PaymentCompleted()

    class Meta:
        ordering = ('-id',)
        
    def __str__(self):
        return str(self.payor)