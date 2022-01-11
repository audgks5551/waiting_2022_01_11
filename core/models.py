from django.db import models

#
from . import managers


class TimeStampedModel(models.Model):

    """ Time Stamped Model """

    created = models.DateTimeField('등록날짜', auto_now_add=True)
    updated = models.DateTimeField('갱신날짜', auto_now=True)
    objects = managers.CustomModelManager()

    class Meta:
        abstract = True
