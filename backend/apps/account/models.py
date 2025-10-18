from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.core.validators import RegexValidator
from .managers import AllUser


class User(AbstractBaseUser):
    numbers = RegexValidator(r"^09\d{9}$", message="Numbers")
    phone = models.CharField(unique=True, max_length=244, validators=[numbers])
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=11, unique=True)
    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    is_active = models.BooleanField(default=True, null=False)
    is_staff = models.BooleanField(default=False, null=False)
    is_superuser = models.BooleanField(default=False, null=False)

    objects = AllUser()

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = ["username", "email"]

    def __str__(self):
        return f"{self.phone}"

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        unique_together = ["phone", "username"]
