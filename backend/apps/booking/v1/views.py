from django.contrib import messages
from django.db import transaction
from django.db.models import F
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render

from apps.booking.models import ReserveService, Schedule

from .forms import ReserveServiceForm


def user_reserve_service_view(request: HttpRequest):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = ReserveServiceForm(request.POST, user=request.user)

            if form.is_valid():
                try:
                    with transaction.atomic():
                        # Get the selected schedule
                        schedule = form.selected_schedule

                        # Get the schedule with row lock
                        locked_schedule = Schedule.objects.select_for_update().get(
                            pk=schedule.pk
                        )

                        if locked_schedule.capacity <= 0:
                            messages.error(
                                request, f"No capacity available for {locked_schedule.date}"
                            )
                            return redirect("booking:user_reserve_service_url")

                        # Create reservation
                        reservation = ReserveService(
                            user=request.user, date=locked_schedule
                        )

                        # Mark that we'll handle capacity update manually
                        reservation._capacity_updated = True
                        reservation.save()

                        # Update capacity atomically - this is the key fix
                        updated = Schedule.objects.filter(
                            pk=locked_schedule.pk,
                            capacity__gt=0,  # Ensure we only update if capacity > 0
                        ).update(capacity=F("capacity") - 1)

                        if updated == 0:
                            # No rows were updated, capacity was 0 or negative
                            reservation.delete()  # Clean up the reservation
                            messages.error(
                                request,
                                "Capacity was exhausted by another user. Please try again.",
                            )
                            return redirect("booking:user_reserve_service_url")

                        messages.success(
                            request, f"Successfully reserved for {locked_schedule.date}!"
                        )
                        return redirect("booking:home")

                except Schedule.DoesNotExist:
                    messages.error(
                        request,
                        "The selected date is no longer available. Please try again.",
                    )
                    return redirect("booking:user_reserve_service_url")
                except Exception as e:
                    messages.error(request, f"An error occurred: {str(e)}")
                    return redirect("booking:user_reserve_service_url")
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field}: {error}")
                return render(request, "booking/reserve.html", {"form": form})
        else:
            form = ReserveServiceForm(user=request.user)
            return render(request, "booking/reserve.html", {"form": form})
    else:
        return redirect("account:login")


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
