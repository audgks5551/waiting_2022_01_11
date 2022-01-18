from django.urls import path, include

#
from . import views
app_name = "stores"

urlpatterns = [
    path("<int:store_id>/", views.detailStore, name="detail"),
    path("create/", views.createStore, name="create"),
    path("", views.listStore, name="list"),
]
