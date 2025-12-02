from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.db.models import F


def booking_view(request: HttpRequest) -> HttpResponse:
    return render(request, "booking/booking_view.html")
