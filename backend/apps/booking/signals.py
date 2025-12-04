from django.core.exceptions import ValidationError
from django.db.models.signals import m2m_changed, pre_delete
from django.dispatch import receiver

from .models import ReserveService


@receiver(pre_delete, sender=ReserveService)
def restore_capacity_on_delete(sender, instance, **kwargs):
    schedule = instance.date
    schedule.capacity += 1
    schedule.save()


@receiver(m2m_changed, sender=ReserveService.service.through)
def update_capacity_on_add(sender, instance, action, **kwargs):
    if action == "post_add":
        schedule = instance.date
        if schedule.capacity >= 0:
            schedule.capacity -= 1
            schedule.save()
        else:
            raise ValidationError("No capacity left!")
