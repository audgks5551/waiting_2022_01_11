from django.urls import path

from . import views

app_name = "waiting"

urlpatterns = [
    path("start/", views.startWaiting, name="start"),
    path("create/", views.createWaiting, name="create"),
]