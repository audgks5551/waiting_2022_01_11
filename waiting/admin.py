from django.contrib import admin

# Register your models here.
from . import models

admin.site.register(models.Waiting)
admin.site.register(models.StartWaiting)
