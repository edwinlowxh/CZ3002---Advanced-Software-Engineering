# Generated by Django 3.2.16 on 2023-03-02 08:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Car', '0009_auto_20230302_0801'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usertrip',
            name='id',
        ),
        migrations.AlterField(
            model_name='usertrip',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL),
        ),
    ]
