from django import forms

from apps.booking.models import ReserveService


class ReserveServiceForm(forms.ModelForm):
    class Meta:
        model = ReserveService
        fields = [
            "date",
        ]
        widgets = {
            # FIXME: Must be Jalali date format
            "data": forms.DateInput(),
        }
