from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User, Profile


class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'username', 'is_active',)
    filter_horizontal = ()
    list_filter = ('is_active',)
    fieldsets = ()
    search_fields = ('email', 'username')
    list_display_links = ('username', 'email')


class AdminProfile(admin.ModelAdmin):
    list_display = ['user', 'email', 'pk']
    search_fields = ('email', 'user')


admin.site.register(User, UserAdmin)

admin.site.register(Profile, AdminProfile)
