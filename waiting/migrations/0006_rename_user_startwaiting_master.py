# Generated by Django 4.0.1 on 2022-01-13 23:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('waiting', '0005_alter_waiting_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='startwaiting',
            old_name='user',
            new_name='master',
        ),
    ]
