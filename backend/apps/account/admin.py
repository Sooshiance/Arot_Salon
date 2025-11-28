from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from apps.account.models import User


class UserAdmin(BaseUserAdmin):
    list_display = ("phone", "email", "username", "is_active")
    filter_horizontal = ()
    list_filter = ("is_active", "is_superuser",)
    fieldsets = ()
    search_fields = ("username",)


admin.site.register(User, UserAdmin)
