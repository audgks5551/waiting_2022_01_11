# Generated by Django 4.0.1 on 2022-01-19 13:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Amenity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='등록날짜')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='갱신날짜')),
                ('name', models.CharField(max_length=80)),
            ],
            options={
                'verbose_name_plural': 'Amenities',
            },
        ),
        migrations.CreateModel(
            name='FoodType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='등록날짜')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='갱신날짜')),
                ('name', models.CharField(max_length=80)),
            ],
            options={
                'verbose_name': 'Food Detail Type',
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.ImageField(blank=True, upload_to='stores/images')),
            ],
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='등록날짜')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='갱신날짜')),
                ('name', models.CharField(max_length=80)),
            ],
            options={
                'verbose_name_plural': 'Menus',
            },
        ),
        migrations.CreateModel(
            name='StoreType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='등록날짜')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='갱신날짜')),
                ('name', models.CharField(max_length=80)),
            ],
            options={
                'verbose_name': 'Food Type',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='등록날짜')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='갱신날짜')),
                ('name', models.CharField(max_length=80)),
            ],
            options={
                'verbose_name_plural': 'Tags',
            },
        ),
        migrations.CreateModel(
            name='Taste',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='등록날짜')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='갱신날짜')),
                ('name', models.CharField(max_length=80)),
            ],
            options={
                'verbose_name_plural': 'Tastes',
            },
        ),
        migrations.CreateModel(
            name='Theme',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='등록날짜')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='갱신날짜')),
                ('name', models.CharField(max_length=80)),
            ],
            options={
                'verbose_name_plural': 'Themes',
            },
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='가게 이름')),
                ('qrcode', models.ImageField(blank=True, upload_to='stores/qrcode/')),
                ('address', models.CharField(default='', max_length=140, verbose_name='가게 주소')),
                ('phone_number', models.CharField(default='', max_length=11, verbose_name='가게 전화번호')),
                ('tags', models.CharField(default='', max_length=200, verbose_name='태그')),
                ('amenities', models.ManyToManyField(blank=True, related_name='stores', to='stores.Amenity')),
                ('food_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='stores', to='stores.foodtype')),
                ('menu', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='stores', to='stores.menu')),
                ('store_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='stores', to='stores.storetype')),
                ('tastes', models.ManyToManyField(blank=True, related_name='stores', to='stores.Taste')),
                ('themes', models.ManyToManyField(blank=True, related_name='stores', to='stores.Theme')),
            ],
        ),
    ]
