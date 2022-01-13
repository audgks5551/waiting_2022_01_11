# Generated by Django 4.0.1 on 2022-01-13 02:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stores', '0006_alter_store_user'),
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
                'verbose_name_plural': 'tags',
            },
        ),
        migrations.AddField(
            model_name='store',
            name='address',
            field=models.CharField(default='', max_length=140, verbose_name='가게 주소'),
        ),
        migrations.AlterField(
            model_name='store',
            name='name',
            field=models.CharField(max_length=30, verbose_name='가게 이름'),
        ),
        migrations.AddField(
            model_name='store',
            name='amenities',
            field=models.ManyToManyField(blank=True, related_name='stores', to='stores.Amenity'),
        ),
        migrations.AddField(
            model_name='store',
            name='food_type',
            field=models.ManyToManyField(blank=True, related_name='stores', to='stores.FoodType'),
        ),
        migrations.AddField(
            model_name='store',
            name='store_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='stores', to='stores.storetype'),
        ),
        migrations.AddField(
            model_name='store',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='stores', to='stores.Tag'),
        ),
    ]
