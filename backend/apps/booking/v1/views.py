from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import F
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render

from apps.booking.models import ReserveService, Schedule

from .forms import ReserveServiceForm


@login_required
def user_reserve_service_view(request: HttpRequest):
    if request.method == "POST":
        form = ReserveServiceForm(request.POST, user=request.user)

        if form.is_valid():
            try:
                with transaction.atomic():
                    # Get the selected date from form
                    selected_date = form.cleaned_data["date"]

                    # Find available schedules for this date with row lock
                    available_schedules = (
                        Schedule.objects.select_for_update()
                        .filter(
                            date=selected_date,
                            capacity__gt=0,
                        )
                        .order_by("capacity")
                    )  # Get the one with most capacity first

                    if not available_schedules.exists():
                        messages.error(
                            request,
                            f"No available services for {selected_date}. Please choose another date.",
                        )
                        return redirect("booking:user_reserve_service_url")

                    # Use the first available schedule
                    schedule = available_schedules.first()

                    # Create reservation
                    reservation = form.save(commit=False)
                    reservation.save()  # This sets the date field to the schedule

                    # Update capacity atomically
                    Schedule.objects.filter(pk=schedule.pk).update(
                        capacity=F("capacity") - 1
                    )

                    messages.success(
                        request,
                        f"Successfully reserved {schedule.service.title} for {selected_date}!",
                    )
                    return redirect("booking:home")

            except ValidationError as e:
                messages.error(request, str(e))
                return redirect("booking:user_reserve_service_url")
            except Exception:
                messages.error(
                    request, "An error occurred during reservation. Please try again."
                )
                return redirect("booking:user_reserve_service_url")
        else:
            # Show form errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
            return render(request, "booking/reservation.html", {"form": form})
    else:
        form = ReserveServiceForm(user=request.user)
        return render(request, "booking/reservation.html", {"form": form})


def user_delete_service_view(
    request: HttpRequest,
    pk: int,
) -> HttpResponseRedirect | HttpResponse:
    if request.user.is_authenticated:
        try:
            # Prevent `Race Condition` situation
            with transaction.atomic():
                reservation = ReserveService.objects.select_for_update().get(
                    pk=pk,
                    user=request.user,
                    activation=True,
                )

                if request.method == "POST":
                    # Double-check we can restore capacity
                    schedule: Schedule = reservation.date

                    reservation.activation = False

                    Schedule.objects.filter(pk=schedule.pk).update(
                        capacity=F("capacity") + 1
                    )

                    messages.success(
                        request,
                        f"Cancelled reservation for {schedule.service.title} on {schedule.date}",
                    )
                    return redirect("user:profile")
                return render(
                    request,
                    "services/delete_reservation.html",
                    {"reservation": reservation},
                )
        except ReserveService.DoesNotExist:
            messages.error(request, "Reservation not found or already cancelled.")
            return redirect("booking:user_delete_service_url")
        except Exception:
            messages.error(request, "An error occurred while processing your request.")
            return redirect("booking:user_delete_service_url")
    else:
        return redirect("account:login")
