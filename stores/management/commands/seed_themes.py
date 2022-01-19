from django.core.management.base import BaseCommand
from stores.models import Theme


class Command(BaseCommand):

    help = "테마 종류 생성"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", help="")

    def handle(self, *args, **options):
        themes = [
            "가성비",
            "가족끼리",
            "간단한",
            "건강빵",
            "고급스러운",
            "관광객",
            "기념일",
            "깨끗한",
            "단체",
            "대화하기 좋은",
            "데이트",
            "몸보신",
            "무한리필",
            "미슐랭",
            "미팅",
            "반주",
            "밥도둑",
            "별미",
            "부모님",
            "불쇼",
            "비주얼",
            "생일",
            "소개팅",
            "소박한",
            "시끌시끌한",
            "신속한",
            "아늑한",
            "웨이팅",
            "음악이 있는",
            "이자카야",
            "인생맛집",
            "인스타용",
            "저렴한",
            "정갈한",
            "제철",
            "조용한",
            "중독성",
            "집밥",
            "치맥",
            "친절한",
            "코스요리",
            "푸짐한",
            "퓨전",
            "피맥",
            "해장",
            "핸드드립",
            "혼밥",
            "회식",
        ]
        for t in themes:
            Theme.objects.create(name=t)
        self.stdout.write(self.style.SUCCESS("Theme created!"))
