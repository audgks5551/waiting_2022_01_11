# Generated by Django 4.0.1 on 2022-01-19 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stores', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='store',
            name='phone_number',
            field=models.CharField(default='', max_length=20, verbose_name='가게 전화번호'),
        ),
    ]
