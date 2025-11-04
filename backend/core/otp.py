import pyotp
from django.http import HttpRequest
from datetime import datetime, timedelta


def sendToken(request: HttpRequest) -> None:
    totp = pyotp.TOTP(pyotp.random_base32(), interval=180)

    otp = totp.now()

    request.session["otp_secret_key"] = totp.secret

    valid_date = datetime.now() + timedelta(minutes=3)

    request.session["otp_valid_date"] = str(valid_date)

    print(f"The OTP is {'=' * 25} : {otp}")
