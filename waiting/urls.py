from django.urls import path

from . import views

app_name = "waiting"

urlpatterns = [
    path("waiting/", views.createWaiting, name="create"),
]