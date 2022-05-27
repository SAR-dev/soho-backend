from django.contrib import admin
from .models import Reward
from django.db import models
from django_json_widget.widgets import JSONEditorWidget

@admin.register(Reward)
class RewardAdmin(admin.ModelAdmin):
    formfield_overrides = {
        # fields.JSONField: {'widget': JSONEditorWidget}, # if django < 3.1
        models.JSONField: {'widget': JSONEditorWidget},
    }