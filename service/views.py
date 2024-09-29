from django.shortcuts import render, redirect, get_object_or_404

from service.models import Category, Service, Rate
from service.forms import UserRate


def home(request):
    c = Category.objects.all().only('title')
    return render(request, "service/index.html", {'category':c})


def eachCategory(request, pk):
    c = Category.objects.get(pk=pk)
    s = Service.objects.filter(category=c.pk).only('title')
    context = {"category":c,"services":s}
    return render(request, "service/category.html", context=context)


def eachService(request, pk):
    s = Service.objects.get(pk=pk)
    r = Rate.objects.get(service=s.pk)
    v = r.each_service_rate()
    context = {'service_rate':v, "service":s}
    return render(request, "service/service.html", context=context)


def giveVote(request, pk):
    if request.user.is_authenticated:
        if request.method == "POST":

            form = UserRate(request.POST)
            s = get_object_or_404(Service, pk=pk)

            if form.is_valid():
                txt = form.cleaned_data['txt']
                vote = form.cleaned_data['vote']

                Rate.objects.create(user=request.user,service=s,vote=vote,txt=txt).save()

                return redirect("service:single-service")
            else:
                return redirect("service:vote")
        else:
            form = UserRate()
        return render(request, "service/rate.html",{'form':form})
    else:
        return redirect("user:login")
