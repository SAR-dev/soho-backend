from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth import get_user_model
User = get_user_model()

class Profile(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    nickname = models.TextField(blank=True)
    date_of_birth = models.DateTimeField(null=True)
    email_address = models.EmailField(blank=True)
    phone_number = models.CharField(max_length=17, blank=True, validators=[
        RegexValidator(
            regex='^\+?1?\d{9,15}$',
            message="Invalid mobile number format! Don't use space.",
        ),
    ])
    website = models.CharField(max_length=100, blank=True, validators=[
        RegexValidator(
            regex='[(http(s)?):\/\/(www\.)?a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)',
            message="Invalid website address format!",
        ),
    ])
    blood_group = models.CharField(max_length=5, blank=True, validators=[
        RegexValidator(
            regex='^(A|B|AB|O)[-+]$',
            message="Invalid blood group!",
        ),
    ])
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    def __str__(self):
        return str(self.user.username)
    
    class Meta:
       ordering = ['-id']
       verbose_name_plural = "profiles"
