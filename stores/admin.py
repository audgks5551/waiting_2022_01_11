from django.contrib import admin
from django.utils.html import mark_safe

from . import models as stores_models
from . import models

@admin.register(models.StoreType, models.FoodType, models.Amenity, models.Tag)
class ItemAdmin(admin.ModelAdmin):

    """ Item Admin Definition """

    list_display = ("name", "used_by")

    def used_by(self, obj):
        return obj.stores.count()

    pass

admin.site.register(stores_models.Store)
