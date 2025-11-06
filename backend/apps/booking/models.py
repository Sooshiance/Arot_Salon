from core.calendar import passed_days
from django.contrib.auth import get_user_model
from django.db import models

from apps.booking.managers import ActiveReservationManager
from apps.service.models import Service

User = get_user_model()


class Departure(models.Model):
    train = models.ForeignKey(Service, on_delete=models.CASCADE)
    date = models.DateField(validators=[passed_days])
    capacity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.train} {self.date} {self.capacity}"


class ReserveService(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.ManyToManyField(Service, blank=True)
    date = models.ForeignKey(Departure, on_delete=models.CASCADE)
    approved = models.BooleanField(default=True)
    admin_approval = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_active = ActiveReservationManager()

    def __str__(self) -> str:
        return f"{self.user} : {self.title}"

    class Meta:
        ordering = ["-updated_at", "-created_at"]
