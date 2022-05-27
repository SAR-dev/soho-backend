from django.contrib import admin
from .models import Group, Category

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    pass

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass