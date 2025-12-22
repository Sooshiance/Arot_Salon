from django.core.exceptions import ValidationError
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from .models import ReserveService


@receiver(pre_delete, sender=ReserveService)
def restore_capacity_on_delete(sender, instance, **kwargs):
    """Restore capacity when reservation is deleted"""
    if hasattr(instance, "_skip_signal") and instance._skip_signal:
        return

    schedule = instance.date
    schedule.capacity += 1
    schedule.save()


@receiver(post_save, sender=ReserveService)
def update_capacity_on_create(sender, instance, created, **kwargs):
    """Update capacity when reservation is created"""
    if not created:
        return

    if hasattr(instance, "_skip_signal") and instance._skip_signal:
        return

    schedule = instance.date
    if schedule.capacity <= 0:
        raise ValidationError("No capacity left!")

    # Only update if we haven't already updated in the view
    if not hasattr(instance, "_capacity_updated"):
        schedule.capacity -= 1
        schedule.save()
        instance._capacity_updated = True
