# Generated by Django 3.2.16 on 2023-02-17 10:06

from django.db import migrations
import django.db.models.manager
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('Transaction', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='transaction',
            managers=[
                ('transaction_manager', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterField(
            model_name='transaction',
            name='type',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('INCOME', 'INCOME'), ('EXPENSE', 'EXPENSE')], max_length=512),
        ),
    ]
