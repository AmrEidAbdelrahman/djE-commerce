# Generated by Django 4.0.1 on 2022-01-05 15:59

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Oreder',
            new_name='Order',
        ),
    ]
