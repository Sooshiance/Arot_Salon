from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, HttpResponse

from apps.service.models import Service


def service_list(request: HttpRequest) -> HttpResponse:
    services = Service.objects.all()
    return render(
        request,
        "service/service_list.html",
        {"services": services},
    )


def service_item(request: HttpRequest, pk: int) -> HttpResponse:
    service = get_object_or_404(Service, pk)
    return render(
        request,
        "service/service_item.html",
        {"service": service},
    )
