from django.contrib import admin
from .models import Warning

@admin.register(Warning)
class WarningAdmin(admin.ModelAdmin):
    pass