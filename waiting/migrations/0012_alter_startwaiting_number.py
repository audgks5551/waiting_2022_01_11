# Generated by Django 4.0.1 on 2022-01-17 02:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('waiting', '0011_startwaiting_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='startwaiting',
            name='number',
            field=models.PositiveSmallIntegerField(default=1, verbose_name='대기번호'),
        ),
    ]
