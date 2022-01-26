from email.policy import default
import random
import csv
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from stores import models as stores_models
from users import models as users_models


class Command(BaseCommand):

    help = "스토어 생성"

    def add_arguments(self, parser):
        parser.add_argument(
            "file_path", type=str, default="example_csv.csv",
        )

    def handle(self, *args, **options):
        file_path = options["file_path"]
        with open(file_path, "r", encoding='utf-8') as csv_file:
            data = list(csv.reader(csv_file, delimiter=","))

        all_users = users_models.User.objects.all()
        store_types = stores_models.StoreType.objects.all()
        food_types = stores_models.FoodType.objects.all()
        menus = stores_models.Menu.objects.all()
        print((lambda x: random.choice(all_users)))

        for row in data[1:1000]:
            stores_models.Store.objects.create(
                name=row[0],
                address=row[1],
                phone_number=row[2],
                store_type=random.choice(store_types),
                food_type=random.choice(food_types),
                menu=random.choice(menus),
                user=random.choice(all_users),
            )
        store_list = stores_models.Store.objects.all()
        amenities = stores_models.Amenity.objects.all()
        themes = stores_models.Theme.objects.all()
        tastes = stores_models.Taste.objects.all()
        for store in store_list:
            for i in range(3, random.randint(10, 30)):
                stores_models.Image.objects.create(
                    store=store,
                    file=f"stores_photos_food/{random.randint(1, 31)}.jpg",
                )

            store.amenities.add("기본")
            store.themes.add("기본")
            store.tastes.add("기본")
            for a in amenities:
                magic_number = random.randint(0, 15)
                if magic_number % 2 == 0:
                    store.amenities.add(a)
            for t in themes:
                magic_number = random.randint(0, 15)
                if magic_number % 2 == 0:
                    store.themes.add(t)
            for t in tastes:
                magic_number = random.randint(0, 15)
                if magic_number % 2 == 0:
                    store.tastes.add(t)

        self.stdout.write(self.style.SUCCESS(f"가게 생성"))
