from django.db import models
from django.contrib.auth.models import UserManager


# 객체가 없으면 none을 반환
class CustomModelManager(models.Manager):
    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except self.model.DoesNotExist:
            return None

# UserManager와 CustomModelManager 합치기
class CustomUserManager(CustomModelManager, UserManager):
    pass