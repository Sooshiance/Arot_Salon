from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.booking.models import ReserveService, Schedule
from apps.service.models import Service

class ReserveServiceForm(forms.ModelForm):
    date = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        }),
        label=_("Select Date")
    )

    class Meta:
        model = ReserveService
        fields = []  # We'll handle date field manually

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Prefetch available schedules with capacity
        available_schedules = Schedule.objects.filter(
            capacity__gt=0,
            date__gte=timezone.now().date()
        ).select_related('service')
        
        # Get unique dates that have available capacity
        self.available_dates = available_schedules.values_list('date', flat=True).distinct()
        
        # Set widget attributes to only show available dates
        if self.available_dates:
            min_date = min(self.available_dates)
            max_date = max(self.available_dates)
            self.fields['date'].widget.attrs.update({
                'min': min_date.isoformat(),
                'max': max_date.isoformat(),
            })

    def clean_date(self):
        selected_date = self.cleaned_data.get('date')
        
        if not selected_date:
            raise ValidationError(_("Please select a date."))
        
        # Check if date is in the future
        if selected_date < timezone.now().date():
            raise ValidationError(_("Cannot reserve for past dates."))
        
        # Check if there are any schedules available for this date
        available_schedules = Schedule.objects.filter(
            date=selected_date,
            capacity__gt=0,
        )
        
        if not available_schedules.exists():
            raise ValidationError(
                _("No available services for %(date)s. Please choose another date."),
                params={'date': selected_date}
            )
        
        # Check if user already has a reservation for this date (any service)
        if self.user and ReserveService.objects.filter(
            user=self.user,
            date__date=selected_date,
            activation=True
        ).exists():
            raise ValidationError(
                _("You already have an active reservation for %(date)s. Please choose another date or cancel your existing reservation."),
                params={'date': selected_date}
            )
        
        # Store the available schedules for this date for later use
        self.available_schedules = available_schedules
        return selected_date

    def save(self, commit=True):
        reservation = super().save(commit=False)
        reservation.user = self.user
        
        # Get the first available schedule for the selected date
        # In a real app, you might want to let users choose which service
        selected_schedule = self.available_schedules.first()
        
        if not selected_schedule:
            raise ValidationError("No available schedule found for the selected date.")
        
        reservation.date = selected_schedule
        
        if commit:
            reservation.save()
        
        return reservation
