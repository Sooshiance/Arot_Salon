from django.contrib import admin

from arot.models import ArotService


class ArotServiceAdmin(admin.ModelAdmin):
    list_display = ('user__username',)


admin.site.register(ArotService, ArotServiceAdmin)
