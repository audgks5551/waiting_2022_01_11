from django.urls import path

from . import views

app_name = "waiting"

urlpatterns = [
    path("", views.listWaiting, name="list"),
    path("detail/<int:startWaiting_id>/", views.detailWaiting, name="detail"),
    path("<int:store_id>/add/", views.addUser, name="add"),
]
