# Generated by Django 3.2.16 on 2023-02-19 04:01

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('Budget', '0002_budget_limit'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='budget',
            managers=[
                ('budget_manager', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterModelManagers(
            name='category',
            managers=[
                ('category_manager', django.db.models.manager.Manager()),
            ],
        ),
    ]
