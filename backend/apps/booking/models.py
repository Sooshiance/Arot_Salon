from core.calendar import passed_days
from django.contrib.auth import get_user_model
from django.db import models

from apps.booking.managers import (
    ActiveReservationManager,
    AdminApprovalManager
)
from apps.service.models import Service

User = get_user_model()


class Schedule(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    date = models.DateField(validators=[passed_days])
    capacity = models.PositiveIntegerField(default=0)

    def __str__(self) -> str:
        return f"{self.service} {self.date} {self.capacity}"


class ReserveService(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ManyToManyField(Service, blank=True)
    date = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    activation = models.BooleanField(default=True)
    admin_approval = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_active = ActiveReservationManager()
    approved = AdminApprovalManager()

    def __str__(self) -> str:
        return f"{self.user}"

    class Meta:
        verbose_name = "Reserve Service"
        verbose_name_plural = "Reserve Services"
        ordering = ["-updated_at", "-created_at"]
        indexes = [
            models.Index(
                fields=[
                    "-updated_at",
                    "-created_at",
                    "activation",
                ],
                name="idx_active_recent_reservations",
            ),
            models.Index(
                fields=["user", "activation", "-updated_at"],
                name="idx_user_active_reservations",
            ),
            models.Index(
                fields=["date", "activation"],
                name="idx_date_active_reservations",
            ),
        ]
