from django.core.management.base import BaseCommand
from stores.models import Amenity


class Command(BaseCommand):

    help = "편의 시설 생성"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", help="")

    def handle(self, *args, **options):
        amenities = [
            "단체석",
            "포장",
            "배달",
            "예약",
            "무선 인터넷",
            "남/녀 화장실 구분",
            "국민지원금",
            "개별룸",
            "라운지",
            "루프탑",
            "발렛",
            "선결제",
            "애완동물반입가능",
            "예약필수",
            "원테이블",
            "좌식",
            "주차",
            "콜키지",
            "콜키지프리",
            "테라스",
            "테이크아웃",
            "한옥집",
            "현금결제",
            "흡연",
        ]
        for a in amenities:
            Amenity.objects.create(name=a)
        self.stdout.write(self.style.SUCCESS("Amenities created!"))
