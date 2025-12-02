from django.urls import path

from .views import booking_view

app_name = "booking"

urlpatterns = [
    path(
        "",
        booking_view,
        name="booking_view",
    ),
]
