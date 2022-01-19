import random
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from stores import models as stores_models
from users import models as user_models


class Command(BaseCommand):

    help = "스토어 생성"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", default=2, type=int, help="How many rooms you want to create"
        )

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()

        all_users = user_models.User.objects.all()
        store_types = stores_models.StoreType.objects.all()
        food_types = stores_models.FoodType.objects.all()
        menus = stores_models.Menu.objects.all()

        seeder.add_entity(
            stores_models.Store,
            number,
            {
                "name": lambda x: seeder.faker.address(),
                "host": lambda x: random.choice(all_users),
                "store_type": lambda x: random.choice(store_types),
                "food_type": lambda x: random.choice(food_types),
                "menu": lambda x: random.choice(menus),
            },
        )
        created_photos = seeder.execute()
        created_clean = flatten(list(created_photos.values()))
        amenities = stores_models.Amenity.objects.all()
        themes = stores_models.Theme.objects.all()
        tastes = stores_models.Taste.objects.all()
        for pk in created_clean:
            store = stores_models.Store.objects.get(pk=pk)
            for i in range(3, random.randint(10, 30)):
                stores_models.Photo.objects.create(
                    store=store,
                    file=f"stores_photos/{random.randint(1, 31)}.webp",
                )
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

        self.stdout.write(self.style.SUCCESS(f"{number} rooms created!"))
