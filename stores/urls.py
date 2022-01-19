from django.urls import path, include

#
from . import views
app_name = "stores"

urlpatterns = [
    path("<int:store_id>/photo/<int:photo_id>/delete/", views.deletePhoto, name="photo_delete"),
    path("<int:store_id>/modify/", views.modifyStore, name="modify"),
    path("<int:store_id>/delete/", views.deleteStore, name="delete"),
    path("<int:store_id>/detail/", views.detailStore, name="detail"),
    path("create/", views.createStore, name="create"),
    path("", views.listStore, name="list"),
]
