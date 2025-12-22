from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.booking.models import ReserveService, Schedule

class ReserveServiceForm(forms.Form):  # Changed to regular Form, not ModelForm
    date = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        }),
        label=_("Select Date")
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Get available dates with capacity
        available_schedules = Schedule.objects.filter(
            capacity__gt=0,
            date__gte=timezone.now().date()
        )
        
        if available_schedules.exists():
            available_dates = available_schedules.values_list('date', flat=True).distinct()
            min_date = min(available_dates)
            max_date = max(available_dates)
            self.fields['date'].widget.attrs.update({
                'min': min_date.isoformat(),
                'max': max_date.isoformat(),
            })
        else:
            # Disable the field if no dates available
            self.fields['date'].widget.attrs['disabled'] = 'disabled'

    def clean_date(self):
        selected_date = self.cleaned_data.get('date')
        
        if not selected_date:
            raise ValidationError(_("Please select a date."))
        
        if selected_date < timezone.now().date():
            raise ValidationError(_("Cannot reserve for past dates."))
        
        # Check if there are available schedules for this date
        available_schedules = Schedule.objects.filter(
            date=selected_date,
            capacity__gt=0,
        )
        
        if not available_schedules.exists():
            raise ValidationError(
                _("No available capacity for %(date)s. Please choose another date."),
                params={'date': selected_date}
            )
        
        # Check for existing reservations on this date (for any schedule)
        if self.user and ReserveService.objects.filter(
            user=self.user,
            date__date=selected_date,
            activation=True
        ).exists():
            raise ValidationError(
                _("You already have an active reservation for %(date)s. Please choose another date or cancel your existing reservation first."),
                params={'date': selected_date}
            )
        
        # Store the first available schedule for this date (you could enhance this to let users choose service)
        self.selected_schedule = available_schedules.first()
        return selected_date
