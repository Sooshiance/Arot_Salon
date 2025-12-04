from typing import Any

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from apps.booking.models import ReserveService, Schedule


class ReserveServiceForm(forms.ModelForm):
    class Meta:
        model = ReserveService
        fields = ["date"]
        widgets = {
            "date": forms.Select(attrs={"class": "form-control"}),
        }

    def __init__(self, *args: Any, **kwargs: Any):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        # Filter available schedules to show only those with capacity > 0
        self.fields["date"].queryset = Schedule.objects.filter(
            capacity__gt=0
        ).select_related("service")

    def clean_date(self):
        date: Schedule = self.cleaned_data.get("date")

        if not date:
            raise ValidationError(_("Please select a valid schedule date."))

        # Check if user already has a reservation for this schedule
        if (
            self.user
            and ReserveService.objects.filter(
                user=self.user,
                date=date,
                activation=True,  # Only check active reservations
            ).exists()
        ):
            raise ValidationError(
                _(
                    "You already have an active reservation for %(service)s on %(date)s. "
                    "Please choose a different date or cancel your existing reservation first."
                ),
                params={"service": date.service.title, "date": date.date},
            )

        # Check capacity (this is a sanity check, the view will handle it atomically)
        if date.capacity <= 0:
            raise ValidationError(
                _(
                    "Sorry, no capacity left for %(service)s on %(date)s. "
                    "Please choose a different schedule."
                ),
                params={"service": date.service.title, "date": date.date},
            )

        return date

    def clean(self):
        cleaned_data = super().clean()

        # Additional validation if needed
        date = cleaned_data.get("date")

        if date and self.user:
            # Double-check the reservation doesn't exist (race condition protection)
            existing_reservation = ReserveService.objects.filter(
                user=self.user, date=date, activation=True
            ).exists()

            if existing_reservation:
                self.add_error(
                    "date",
                    ValidationError(
                        _("A reservation for this schedule already exists."),
                        code="duplicate_reservation",
                    ),
                )

        return cleaned_data
