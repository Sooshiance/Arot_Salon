from django.urls import path

from service import views


app_name = "service"

urlpatterns = [
    path("", views.home, name='home'),
    path("<int:pk>/",views.eachCategory, name='category'),
    path("service/<int:pk>/", views.eachService, name='single-service'),
    path("vote/<int:pk>/", views.giveVote, name='vote'),
]
