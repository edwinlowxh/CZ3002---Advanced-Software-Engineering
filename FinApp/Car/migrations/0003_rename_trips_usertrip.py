# Generated by Django 3.2.16 on 2023-02-12 13:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0003_delete_userinformation'),
        ('Car', '0002_alter_car_managers'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Trips',
            new_name='UserTrip',
        ),
    ]
