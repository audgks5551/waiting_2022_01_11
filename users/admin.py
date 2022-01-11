from django.contrib import admin

# Register your models here.
from . import models as accounts_models

admin.site.register(accounts_models.User)