from typing import Any, Literal

from django.contrib.auth.models import AbstractBaseUser
from django.core.validators import RegexValidator
from django.db import models

from .managers import AllUser


class User(AbstractBaseUser):
    numbers = RegexValidator(r"^09\d{9}$", message="Numbers")
    phone = models.CharField(unique=True, max_length=244, validators=[numbers])
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    is_active = models.BooleanField(default=True, null=False)
    is_staff = models.BooleanField(default=False, null=False)
    is_superuser = models.BooleanField(default=False, null=False)

    objects = AllUser()

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = ["username", "email"]

    def __str__(self) -> str:
        return f"{self.phone}"

    def has_perm(self, perm, obj=None) -> Literal[True]:
        return True

    def has_module_perms(self, app_label: Any) -> Literal[True]:
        return True

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    first_name = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self)->str:
        return f"{self.user.phone}"
