from django import forms 

from .models import User


class UserRegister(forms.ModelForm):
    class Meta:
        model = User 
        fields = ['phone', 'password', 'first_name', 'last_name']
        labels = {
            "phone": "شماره همراه",
            "password": "گذر واژه",
            "first_name": "نام",
            "last_name": "نام خانوادگی",
        }
        widgets = {
            "phone": forms.NumberInput(attrs={'class':'form-control my-5'}),
            "password": forms.PasswordInput(attrs={'class':'form-control my-5'}),
            "first_name": forms.TextInput(attrs={'class':'form-control my-5'}),
            "last_name": forms.TextInput(attrs={'class':'form-control my-5'}),
        }


class LoginForm(forms.Form):
    phone    = forms.CharField(label="Phone", max_length=11)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)


class OTPForm(forms.Form):
    otp = forms.CharField(label="OTP", max_length=6)
