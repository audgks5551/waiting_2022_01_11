# Generated by Django 4.0.1 on 2022-01-19 02:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('stores', '0010_alter_store_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='store',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stores', to=settings.AUTH_USER_MODEL),
        ),
    ]
