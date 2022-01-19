from django.core.management.base import BaseCommand
from stores.models import Taste


class Command(BaseCommand):

    help = "맛 종류 생성"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", help="")

    def handle(self, *args, **options):
        tastes = [
            "개운한",
            "걸쭉한",
            "고소한",
            "구수한",
            "깔끔한",
            "느끼한",
            "달콤한",
            "담백한",
            "두툼한",
            "따끈한",
            "뜨거운",
            "매운",
            "매콤달콤한",
            "바삭한",
            "부드러운",
            "산뜻한",
            "상큼한",
            "새콤달콤한",
            "새콤한",
            "순한",
            "신맛이 나는",
            "신선한",
            "심심한",
            "싱거운",
            "쌉싸름한",
            "쓴맛이 나는",
            "알싸한",
            "은은한",
            "자극적",
            "진득한",
            "진한",
            "짠맛이 나는",
            "쫀득한",
            "쫄깃한",
            "촉촉한",
            "텁텁한",
            "향긋한",
        ]
        for t in tastes:
            Taste.objects.create(name=t)
        self.stdout.write(self.style.SUCCESS("Taste created!"))
