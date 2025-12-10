from django.urls import path

from .views import user_delete_service_view, user_reserve_service_view

app_name = "booking"

urlpatterns = [
    path(
        "",
        user_reserve_service_view,
        name="user_reserve_service_url",
    ),
    path(
        "<int:pk>/",
        user_delete_service_view,
        name="user_delete_service_url",
    ),
]
