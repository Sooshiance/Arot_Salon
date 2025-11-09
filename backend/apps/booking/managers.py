from django.db import models
from django.db.models import QuerySet


class ActiveReservationManager(models.Manager):
    """Manager to soft delete user reservation"""

    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(activation=True)


class AdminApprovalManager(models.Manager):
    """Manager to soft delete user reservation by admin"""

    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(admin_approval=True)
