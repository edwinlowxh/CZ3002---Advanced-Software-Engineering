# Generated by Django 3.2.16 on 2023-02-23 04:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0002_auto_20230210_1758'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userinformation',
            old_name='birth_date',
            new_name='date_of_birth',
        ),
    ]