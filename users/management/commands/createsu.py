from django.core.management.base import BaseCommand
from users.models import User


class Command(BaseCommand):

    help = "슈퍼 유저 생성"

    def handle(self, *args, **options):
        admin = User.objects.get_or_none(username="admin@admin.com")
        if not admin:
            User.objects.create_superuser(
                "admin@admin.com", "admin@admin.com", "123456")
            self.stdout.write(self.style.SUCCESS(f"슈퍼유저생성"))
        else:
            self.stdout.write(self.style.SUCCESS(f"슈퍼유저 이미 존재"))
