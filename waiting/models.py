from django.db import models

#
from core import models as core_models
from users.models import User
from stores.models import Store


class StartWaiting(core_models.TimeStampedModel):

    store = models.ForeignKey(
        Store, related_name="startWaitings", on_delete=models.CASCADE)
    master = models.ForeignKey(
        User, related_name="startWaitings", on_delete=models.CASCADE)
    wait_time = models.PositiveSmallIntegerField("한 테이블 당 식사시간")
    table_number = models.PositiveSmallIntegerField("테이블 수")
    number = models.PositiveSmallIntegerField("대기번호", default=1)
    mode = models.BooleanField(default=False)


class Waiting(core_models.TimeStampedModel):

    number = models.PositiveSmallIntegerField("대기번호")
    time = models.PositiveSmallIntegerField("대기시간")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    startWaiting = models.ForeignKey(
        StartWaiting, related_name="waitings", on_delete=models.CASCADE)
    people_number = models.PositiveSmallIntegerField("인원수")
