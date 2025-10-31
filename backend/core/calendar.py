from datetime import date as Date

from django.core.exceptions import ValidationError
from django.utils import timezone


def passed_days(day: Date) -> Date:
    if day < timezone.now().date():
        raise ValidationError("It's passed!")
    else:
        return day
