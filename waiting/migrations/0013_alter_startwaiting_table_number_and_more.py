# Generated by Django 4.0.1 on 2022-01-18 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('waiting', '0012_alter_startwaiting_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='startwaiting',
            name='table_number',
            field=models.PositiveSmallIntegerField(verbose_name='테이블 수'),
        ),
        migrations.AlterField(
            model_name='startwaiting',
            name='wait_time',
            field=models.PositiveSmallIntegerField(verbose_name='한 테이블 당 식사시간'),
        ),
    ]
