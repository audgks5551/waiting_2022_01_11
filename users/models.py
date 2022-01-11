from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from django.conf import settings
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.template.loader import render_to_string
#
from core import managers  as base_managers

class User(AbstractUser):

    """ Custom User Model """

    class GenderChoices(models.TextChoices):
        MALE    = "M", "Male"
        FEMALE  = "F", "Female"
    
    class LoginChoices(models.TextChoices):
        EMAIL = "email", "Email"
        GITHUB = "github", "Github"
        KAKAO = "kakao", "Kakao"

    first_name      = models.CharField("이름", max_length=30, blank=True, default="")
    avatar          = models.ImageField(blank=True, upload_to="users/avatar/%Y/%m/%d")
    gender          = models.CharField("성별", max_length=1, blank=True, choices=GenderChoices.choices)
    objects         = base_managers.CustomUserManager()
    email_verified  = models.BooleanField(default=False)
    email_secret    = models.CharField(max_length=120, default="", blank=True)
    login_method    = models.CharField(max_length=50, choices=LoginChoices.choices, default=LoginChoices.EMAIL)

    def verify_email(self):
        if self.email_verified is False:
            secret = uuid.uuid4().hex[:20]
            self.email_secret = secret
            html_message = render_to_string("emails/verify_email.html", {"secret": secret})
            send_mail(
                "Verify it's easy Account",
                strip_tags(html_message),
                settings.EMAIL_FROM,
                [self.email],
                fail_silently=False,
                html_message=html_message,
            )
            self.save()
        return

