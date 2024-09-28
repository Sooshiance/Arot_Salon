from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User, Profile


class UserAdmin(BaseUserAdmin):
    list_display = ('phone', 'username', 'is_active',)
    filter_horizontal = ()
    list_filter = ('is_active',)
    fieldsets = ()
    search_fields = ('phone', 'username')
    list_display_links = ('username', 'phone')


class AdminProfile(admin.ModelAdmin):
    list_display = ['user', 'phone', 'pk']
    search_fields = ('phone', 'user')


admin.site.register(User, UserAdmin)

admin.site.register(Profile, AdminProfile)
