from django.urls import path

from user import views


app_name = "user"

urlpatterns = [
    path("", views.loginUser, name="login"),
    path("logout/", views.logoutUser, name='logout'),
    path("register/", views.registerUser, name='register'),
    path("register/otp/", views.otpRegisterValidation, name='otp_register'),
    path("profile/", views.userProfile, name='profile'),

    # TODO: Password resetting
    path("reset-password/", views.otpPassworReset, name="reset_password"),
    path("check-otp/", views.checkOTP, name='check_otp'),
    path("change-password/", views.confirmResetPassowrd, name='new_password'),
]
