from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import F
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render

from apps.booking.models import ReserveService, Schedule
from apps.booking.v1.forms import ReserveServiceForm


@login_required
def user_reserve_service_view(
    request: HttpRequest,
) -> HttpResponse | HttpResponseRedirect:
    if request.method == "POST":
        form = ReserveServiceForm(request.POST, user=request.user)

        if form.is_valid():
            try:
                with transaction.atomic():
                    # Get the schedule with row lock
                    schedule = Schedule.objects.select_for_update().get(
                        pk=form.cleaned_data["date"].pk
                    )

                    # Final capacity check (atomic operation)
                    if schedule.capacity <= 0:
                        messages.error(
                            request,
                            f"No capacity available for {schedule.service.title} on {schedule.date}",
                        )
                        return redirect("services:reserve")

                    # Create reservation
                    reservation = form.save(commit=False)
                    reservation.user = request.user
                    reservation.save()

                    # Update capacity atomically
                    Schedule.objects.filter(pk=schedule.pk).update(
                        capacity=F("capacity") - 1
                    )

                    messages.success(
                        request,
                        f"Successfully reserved {schedule.service.title} for {schedule.date}!",
                    )
                    return redirect("services:home")

            except Schedule.DoesNotExist:
                messages.error(
                    request,
                    "The selected schedule is no longer available. Please try again.",
                )
                return redirect("services:reserve")
            except ValidationError as e:
                messages.error(request, str(e))
                return redirect("services:reserve")
            except Exception:
                messages.error(
                    request, "An unexpected error occurred. Please try again."
                )
                return redirect("services:reserve")
        else:
            # Form has errors - show them to the user
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
            return render(request, "services/reserve.html", {"form": form})
    else:
        form = ReserveServiceForm(user=request.user)
        return render(request, "services/reserve.html", {"form": form})


@login_required
def user_delete_service_view(
    request: HttpRequest,
    pk: int,
) -> HttpResponseRedirect | HttpResponse:
    try:
        with transaction.atomic():
            # Get the reservation with select_for_update to prevent race conditions
            reservation = ReserveService.objects.select_for_update().get(
                pk=pk,
                user=request.user,
                activation=True,
            )

            if request.method == "POST":
                # Double-check we can restore capacity
                schedule: Schedule = reservation.date

                # Delete the reservation
                reservation.delete()

                # Restore capacity atomically
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
        return redirect("user:profile")
    except Exception:
        messages.error(request, "An error occurred while processing your request.")
        return redirect("user:profile")
