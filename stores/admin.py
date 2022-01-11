from django.contrib import admin

from . import models as stores_models

admin.site.register(stores_models.Store)
