from django.db import models

#
from users.models import User

class Store(models.Model):
    name = models.CharField('가게명', max_length=30)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)