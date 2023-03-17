# Generated by Django 3.2.16 on 2023-03-16 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Car', '0011_alter_usertrip_trips'),
    ]

    operations = [
        migrations.AddField(
            model_name='trip',
            name='destination_latitude',
            field=models.CharField(default='exit', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='trip',
            name='destination_longitude',
            field=models.CharField(default='exit', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='trip',
            name='source_latitude',
            field=models.CharField(default='exit', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='trip',
            name='source_longitude',
            field=models.CharField(default='exit', max_length=255),
            preserve_default=False,
        ),
    ]
