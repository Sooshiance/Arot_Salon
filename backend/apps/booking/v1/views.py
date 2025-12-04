from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import F
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render

from apps.booking.models import ReserveService, Schedule
from apps.booking.v1.forms import ReserveServiceForm


def user_reserve_service_view(
    request: HttpRequest,
) -> HttpResponseRedirect | HttpResponse:
    if request.user.is_authenticated:
        if request.method == "POST":
            form = ReserveServiceForm(request.POST)
            if form.is_valid():
                try:
                    # Use atomic transaction to prevent race conditions
                    with transaction.atomic():
                        # Get the schedule with row lock using select_for_update
                        schedule_id = form.cleaned_data["date"].id
                        schedule = Schedule.objects.select_for_update().get(
                            id=schedule_id
                        )

                        # Check capacity with the locked row
                        if schedule.capacity <= 0:
                            messages.error(
                                request,
                                f"No capacity left for {schedule.service.title} on {schedule.date}",
                            )
                            return redirect("services:reserve")

                        # Create reservation
                        reservation = form.save(commit=False)
                        reservation.user = request.user
                        reservation.save()

                        # Update capacity atomically using F() expression
                        Schedule.objects.filter(id=schedule_id).update(
                            capacity=F("capacity") - 1
                        )

                        messages.success(request, "Reservation created successfully!")
                        return redirect("services:home")

                except Schedule.DoesNotExist:
                    messages.error(
                        request, "The selected schedule is no longer available."
                    )
                    return redirect("services:reserve")
                except ValidationError as e:
                    messages.error(request, str(e))
                    return redirect("services:reserve")
            else:
                messages.error(request, "Please correct the errors in the form.")
                return render(request, "services/reserve.html", {"form": form})
        else:
            form = ReserveServiceForm()
            return render(request, "services/reserve.html", {"form": form})
    else:
        return redirect("account:login")


def user_delete_service_view(
    request: HttpRequest, pk: int
) -> HttpResponseRedirect | HttpResponse:
    if request.user.is_authenticated:
        if request.method == "POST":
            try:
                with transaction.atomic():
                    # Get the reservation and lock related schedule
                    reservation = get_object_or_404(
                        ReserveService,
                        pk=pk,
                        user=request.user,
                    )
                    schedule = Schedule.objects.select_for_update().get(
                        id=reservation.date.id
                    )

                    # Delete the reservation
                    reservation.delete()

                    # Restore capacity atomically
                    Schedule.objects.filter(id=schedule.id).update(
                        capacity=F("capacity") + 1
                    )

                    messages.success(request, "Reservation cancelled successfully!")
                    return redirect("user:profile")

            except ReserveService.DoesNotExist:
                messages.error(
                    request,
                    "Reservation not found or you don't have permission to delete it.",
                )
                return redirect("user:profile")
            except Exception:
                messages.error(
                    request, "An error occurred while cancelling your reservation."
                )
                return redirect("user:profile")

        # GET request - show confirmation page
        try:
            reservation = get_object_or_404(ReserveService, pk=pk, user=request.user)
            return render(
                request,
                "services/delete_reservation.html",
                {"reservation": reservation},
            )
        except ReserveService.DoesNotExist:
            messages.error(request, "Reservation not found.")
            return redirect("user:profile")
    else:
        return redirect("account:login")
