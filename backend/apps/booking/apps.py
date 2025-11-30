from django.apps import AppConfig


class BookingConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.booking"

    def ready(self):
        import apps.booking.signals   # noqa: F401
