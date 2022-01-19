from django.core.management.base import BaseCommand
from stores.models import FoodType


class Command(BaseCommand):

    help = "음식 종류 생성"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", help="")

    def handle(self, *args, **options):
        foodTypes = [
            "양식",
            "일식",
            "중식",
            "한식",
            "세계음식",
            "뷔페",
            "카페",
            "주점",
        ]
        for f in foodTypes:
            FoodType.objects.create(name=f)
        self.stdout.write(self.style.SUCCESS("FoodType created!"))
