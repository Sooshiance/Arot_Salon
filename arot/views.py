from django.shortcuts import render, redirect

from arot.forms import Reserve


def reserveService(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = Reserve(request.POST)

            if form.is_valid():
                user_form = form.save(commit=False)

                user_form.user = request.user

                user_form.save()

                return redirect("service:home")
            else:
                return redirect("arot:reserve")
        else:
            form = Reserve()
        return render(request, "arot/reserve.html", {'form':form})
    else:
        return redirect("user:login")
