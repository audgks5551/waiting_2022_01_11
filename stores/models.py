from django.db import models

#
from users.models import User

class Store(models.Model):
    name    = models.CharField('가게명', max_length=30)
    qrcode  = models.ImageField(blank=True, upload_to="stores/qrcode/%Y/%m/%d")
    user    = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    def __str__(self):
        return str(f"{self.name}")