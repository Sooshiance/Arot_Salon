# TODO: Forget password scenarios

from django.contrib import auth, messages
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponsePermanentRedirect,
    HttpResponseRedirect,
)
from django.shortcuts import redirect, render

from apps.account.models import Profile, User
from apps.account.v1.forms import LoginForm, RegisterForm


def login_user(
    request: HttpRequest,
) -> HttpResponseRedirect | HttpResponsePermanentRedirect | HttpResponse:
    if request.user.is_authenticated:
        messages.warning(request, "not this one")
        return redirect("service:home")
    elif request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data["phone"]
            password = form.cleaned_data["password"]

            user = auth.authenticate(
                request,
                phone=phone,
                password=password,
            )

            if user is not None:
                auth.login(request, user)
                return redirect("service:home")
            else:
                messages.error(
                    request,
                    "مشخصات وارد شده اشتباه می باشد، دوباره تلاش کنید",
                )
                return render(
                    request,
                    "account/login.html",
                    {"form": form},
                    status=401,
                )
        else:
            return render(
                request,
                "account/login.html",
                {"form": form},
                status=401,
            )
    else:
        form = LoginForm()
    return render(
        request,
        "account/login.html",
        {"form": form},
    )


def logout_user(
    request: HttpRequest,
) -> HttpResponseRedirect | HttpResponsePermanentRedirect:
    auth.logout(request)
    messages.info(request, "به امید دیداری دوباره")
    return redirect("account:login")


def register_user(
    request: HttpRequest,
) -> HttpResponseRedirect | HttpResponsePermanentRedirect | HttpResponse:
    if request.user.is_authenticated:
        messages.warning(request, "شما نمیتوانید به این صفحه مراجعه کنید")
        return redirect("service:home")
    elif request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data["phone"]
            email = form.cleaned_data["email"]
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            user = User.objects.create_user(
                phone=phone,
                email=email,
                username=username,
                password=password,
            )
            user.set_password(password)
            messages.success(request, "اطلاعات شما با موفقیت ثبت گردید")
            return redirect("account:login")
        else:
            messages.error(request, f"{form.errors}")
            return render(
                request,
                "account/register.html",
                {"form": form},
                status=401,
            )
    else:
        form = RegisterForm()
    return render(request, "account/register.html", {"form": form})


def profile_view(request: HttpRequest) -> HttpResponse | HttpResponseRedirect:
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        return render(
            request,
            "account/profile.html",
            {"profile": profile},
        )
    else:
        return redirect("account:login")
