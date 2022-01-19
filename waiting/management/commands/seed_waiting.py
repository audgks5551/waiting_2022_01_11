import random
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from waiting import models as waiting_models
from stores import models as stores_models
from users import models as users_models


class Command(BaseCommand):

    help = "waiting start 생성"

    def handle(self, *args, **options):
        stores = stores_models.Store.objects.all()

        for store in stores:
            master = users_models.User.objects.get(id=store.user_id)
            w = waiting_models.StartWaiting(
                store=store,
                wait_time=30,
                table_number=30,
                master=master
            )
            w.save()

        self.stdout.write(self.style.SUCCESS("start waiting 생성!!"))
