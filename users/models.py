from django.db import models
from django.contrib.auth.models import AbstractUser

#
from core import managers  as base_managers

class User(AbstractUser):

    """ Custom User Model """

    class GenderChoices(models.TextChoices):
        MALE    = "M", "Male"
        FEMALE  = "F", "Female"

    first_name = models.CharField("이름", max_length=30, blank=True, default="")
    avatar = models.ImageField(blank=True, upload_to="accounts/avatar/%Y/%m/%d")
    objects = base_managers.CustomUserManager()

