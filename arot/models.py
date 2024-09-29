from django.db import models
from django.conf import settings

from arot.enums import Label
from arot.utils import passedDay, noFriday


class ArotService(models.Model):
    description = models.TextField(blank=True, null=True)
    service = models.PositiveSmallIntegerField(choices=Label.choices())
    date = models.DateField(validators=[passedDay, noFriday])
    user = models.ForeignKey(settings.AUTH_USERMODEL, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.user}"
    
    class Meta:
        verbose_name = 'Arot Service'
        verbose_name_plural = 'Arot Services'
