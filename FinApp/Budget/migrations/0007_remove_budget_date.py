# Generated by Django 3.2.16 on 2023-02-26 08:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Budget', '0006_auto_20230226_0805'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='budget',
            name='date',
        ),
    ]
