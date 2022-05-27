from django.contrib import admin
from .models import Choice

# Register your models here.
@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('text',)