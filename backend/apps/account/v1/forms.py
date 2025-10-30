from core.validators import iranian_phone_number_normalizer
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from apps.account.models import User


class RegisterForm(UserCreationForm):
    password = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control my-5",
                "placeholder": "••••••••••••",
            }
        )
    )
    password2 = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control my-5",
                "placeholder": "••••••••••••",
            }
        )
    )

    class Meta:
        model = User

        fields = [
            "phone",
            "username",
            "email",
            "first_name",
            "last_name",
        ]

        labels = {
            "password": "گذر واژه",
            "password2": "تکرار گذر واژه",
        }

        widgets = {
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control my-5",
                    "placeholder": "example1234@gmail.com",
                }
            ),
            "phone": forms.NumberInput(
                attrs={"class": "form-control my-5", "placeholder": "09123456789"}
            ),
            "username": forms.TextInput(
                attrs={"class": "form-control my-5", "placeholder": "Username"}
            ),
            "password": forms.PasswordInput(
                attrs={"class": "form-control my-5", "placeholder": "••••••••••••"}
            ),
            "password2": forms.PasswordInput(
                attrs={"class": "form-control my-5", "placeholder": "••••••••••••"}
            ),
            "first_name": forms.TextInput(
                attrs={"class": "form-control my-5", "placeholder": "zari"}
            ),
            "last_name": forms.TextInput(
                attrs={"class": "form-control my-5", "placeholder": "alizadeh"}
            ),
        }

    def clean(self) -> None:
        cleaned_data = super(RegisterForm, self).clean()
        password = cleaned_data["password"]
        password2 = cleaned_data["password2"]
        if password != password2:
            raise ValidationError("Passwords are not match!")

    def clean_phone(self) -> str | None:
        cleaned_data = super(RegisterForm, self).clean()
        phone = cleaned_data.get("phone")

        normalized_phone = iranian_phone_number_normalizer(phone)

        if normalized_phone == "Error":
            raise ValidationError("Phone is not an iranian phone number")
        return normalized_phone


class LoginForm(forms.Form):
    phone = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control my-5", "placeholder": "09123456789"}
        )
    )
    password = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control my-5", "placeholder": "••••••••••••"}
        )
    )
