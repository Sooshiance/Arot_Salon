from django.urls import path

from arot.views import reserveService


app_name = "arot"

urlpatterns = [
    path("", reserveService, name='reserve'),
]
