from django.urls import path

from . import views

app_name = "waiting"

urlpatterns = [
    path("", views.listWaiting, name="list"),
    path("detail/<int:startWaiting_id>/", views.detailWaiting, name="detail"),
    path("<int:store_id>/add/", views.addUser, name="add"),
    path("<int:waiting_id>/remove/", views.removeUser, name="remove"),
    path("<int:startWaiting_id>/start", views.startMode, name="start"),
    path("<int:startWaiting_id>/stop", views.stopMode, name="stop"),
    path("<int:startWaiting_id>/reset", views.resetMode, name="reset"),
]
