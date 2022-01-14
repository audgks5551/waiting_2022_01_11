from django.urls import path

from . import views

app_name = "waiting"

urlpatterns = [
    path("", views.listWaiting, name="list"),
    path("start/<int:startWaiting_id>/", views.detailWaiting, name="detail"),
    path("<int:store_id>/create/", views.createWaiting, name="create"),
]