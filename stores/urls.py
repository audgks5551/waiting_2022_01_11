from django.urls import path, include

#
from . import views
app_name = "stores"

urlpatterns = [
    path("", views.storeList, name="list"),
]