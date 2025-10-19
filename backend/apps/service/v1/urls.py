from django.urls import path

from .views import service_item, service_list


app_name = "service"

urlpatterns = [
    path(
        "",
        service_list,
        name="home",
    ),
    path(
        "<pk:int>/",
        service_item,
        name="service",
    ),
]
