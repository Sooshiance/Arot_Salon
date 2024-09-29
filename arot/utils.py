from django.utils import timezone
from django.core.exceptions import ValidationError
from psycopg2 import Date


def passedDay(obj):
    if obj < timezone.now():
        raise ValidationError("")
    return True


def noFriday(obj:Date):
    if obj.weekday()==4:
        raise ValidationError("")
    return True
