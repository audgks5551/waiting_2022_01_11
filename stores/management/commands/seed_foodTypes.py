from django.core.management.base import BaseCommand
from stores.models import FoodType


class Command(BaseCommand):

    help = "음식 종류 생성"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", help="")

    def handle(self, *args, **options):
        foodTypes = [
            "고기 요리",
            "국수/면 요리",
            "기타 한식",
            "닭/오리 요리",
            "탕/찌개/전골",
            "퓨전 한식",
            "한정식/백반/정통 한식",
            "해산물 요리",
            "기타 중식",
            "딤섬/만두",
            "정통 중식/일반 중식",
            "퓨전 중식",
            "기타 일식",
            "까스 요리",
            "돈부리/일본 카레/벤토",
            "라멘/소바/우동",
            "이자카야/오뎅/꼬치",
            "정통 일식/일반 일식",
            "철판 요리",
            "퓨전 일식",
            "회/스시",
            "기타 양식",
            "브런치/버거/샌드위치",
            "스테이크/바베큐",
            "시푸드 요리",
            "이탈리안",
            "패밀리 레스토랑",
            "퓨전 양식",
            "프랑스 음식",
            "남미 음식",
            "다국적 아시아 음식",
            "다국적 퓨전",
            "베트남 음식",
            "세계음식 기타",
            "인도 음식",
            "태국 음식",
            "뷔페",
            "베이커리",
            "카페/디저트",
            "일반 주점",
            "전통 주점/포차",
            "치킨/호프/펍",
            "칵테일/와인",
        ]
        for f in foodTypes:
            FoodType.objects.create(name=f)
        self.stdout.write(self.style.SUCCESS("FoodType created!"))
