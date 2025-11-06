from django.db import models
from django.db.models import QuerySet


class ActiveReservationManager(models.Manager):
    """Manager to soft delete user reservation"""

    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(is_active=True)
