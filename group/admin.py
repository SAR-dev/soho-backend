from django.contrib import admin
from .models import Group, Category, SubCategory

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    pass

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    pass