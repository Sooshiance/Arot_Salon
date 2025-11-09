from django.contrib import admin

from .models import ReserveService, Schedule


class ScheduleAdmin(admin.ModelAdmin):
    list_display = ("service",)


class ReserveServiceAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "activation",
        "admin_approval",
    )
    list_filter = (
        "activation",
        "admin_approval",
    )


admin.site.register(Schedule, ScheduleAdmin)


admin.site.register(ReserveService, ReserveServiceAdmin)
