from django.contrib import admin
from .models import Moderator

@admin.register(Moderator)
class ModeratorAdmin(admin.ModelAdmin):
    pass