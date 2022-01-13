from django.db import models

#
from core import models as core_models
from users.models import User
from stores.models import Store

class StartWaiting(core_models.TimeStampedModel):

        store   = models.ForeignKey(Store, on_delete=models.CASCADE)
        user    = models.ForeignKey(User, on_delete=models.CASCADE)

class Waiting(core_models.TimeStampedModel):

        number              = models.PositiveSmallIntegerField("대기번호")
        time                = models.PositiveSmallIntegerField("대기시간")
        user                = models.ForeignKey(User, on_delete=models.CASCADE)
        startWaiting        = models.ForeignKey(StartWaiting, on_delete=models.CASCADE)
    



