from django.contrib import admin

from .models import Departure, ReserveService


class DepartureAdmin(admin.ModelAdmin):
    list_display = ("train",)


class ReserveServiceAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "is_active",
        "admin_approval",
    )
    list_filter = (
        "is_active",
        "admin_approval",
    )


admin.site.register(Departure, DepartureAdmin)


admin.site.register(ReserveService, ReserveServiceAdmin)
