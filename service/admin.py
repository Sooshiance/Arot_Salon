from django.contrib import admin

from service.models import Category, Service, Rate


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)


admin.site.register(Category, CategoryAdmin)


class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title',)


admin.site.register(Service, ServiceAdmin)


class RateAdmin(admin.ModelAdmin):
    list_display = ('user__username',)


admin.site.register(Rate, RateAdmin)
