from django.contrib import admin
from .models import Award

# Register your models here.
@admin.register(Award)
class AwardeAdmin(admin.ModelAdmin):
    list_display = ('name',)