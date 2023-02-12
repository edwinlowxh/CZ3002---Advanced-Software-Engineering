# Generated by Django 3.2.16 on 2023-02-11 02:32

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('House', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='housinguserdata',
            managers=[
                ('housing_data_manager', django.db.models.manager.Manager()),
            ],
        ),
        migrations.RenameField(
            model_name='housinguserdata',
            old_name='estimatedMonthlySavings',
            new_name='estimated_monthly_savings',
        ),
        migrations.RenameField(
            model_name='housinguserdata',
            old_name='preferredLocation',
            new_name='preferred_property_location',
        ),
        migrations.RenameField(
            model_name='housinguserdata',
            old_name='preferredPropertyType',
            new_name='preferred_property_type',
        ),
    ]