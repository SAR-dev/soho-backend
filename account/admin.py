from django.contrib import admin
from .models import Account

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'is_admin', 'is_staff', )
    readonly_fields = ('id', 'date_joined', 'last_login', )