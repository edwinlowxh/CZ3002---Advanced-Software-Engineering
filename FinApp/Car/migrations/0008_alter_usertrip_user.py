# Generated by Django 3.2.16 on 2023-03-02 07:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0003_delete_userinformation'),
        ('Car', '0007_alter_usertrip_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usertrip',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='Main.user'),
        ),
    ]
