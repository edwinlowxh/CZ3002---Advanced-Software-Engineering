# Generated by Django 3.2.16 on 2023-02-23 05:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0003_rename_birth_date_userinformation_date_of_birth'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinformation',
            name='date_of_birth',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='userinformation',
            name='marital_status',
            field=models.CharField(max_length=7, null=True),
        ),
    ]