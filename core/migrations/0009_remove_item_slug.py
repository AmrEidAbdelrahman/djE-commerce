# Generated by Django 4.0.1 on 2022-01-05 22:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_alter_item_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='slug',
        ),
    ]
