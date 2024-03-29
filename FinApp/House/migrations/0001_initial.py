# Generated by Django 3.2.16 on 2023-02-11 02:20

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager
import multiselectfield.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Main', '0003_delete_userinformation'),
    ]

    operations = [
        migrations.CreateModel(
            name='HousingUserData',
            fields=[
                ('user', models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='Main.user')),
                ('preferredPropertyType', multiselectfield.db.fields.MultiSelectField(choices=[('1 ROOM', '1 ROOM'), ('2 ROOM', '2 ROOM'), ('3 ROOM', '3 ROOM'), ('4 ROOM', '4 ROOM'), ('5 ROOM', '5 ROOM'), ('EXECUTIVE', 'EXECUTIVE'), ('MULTI-GENERATION', 'MULTI-GENERATION')], max_length=512)),
                ('estimatedMonthlySavings', models.FloatField()),
                ('preferredLocation', multiselectfield.db.fields.MultiSelectField(choices=[('ANG MO KIO', 'ANG MO KIO'), ('BEDOK', 'BEDOK'), ('BISHAN', 'BISHAN'), ('BUKIT BATOK', 'BUKIT BATOK'), ('BUKIT MERAH', 'BUKIT MERAH'), ('BUKIT PANJANG', 'BUKIT PANJANG'), ('BUKIT TIMAH', 'BUKIT TIMAH'), ('CENTRAL AREA', 'CENTRAL AREA'), ('CHOA CHU KANG', 'CHOA CHU KANG'), ('CLEMENTI', 'CLEMENTI'), ('GEYLANG', 'GEYLANG'), ('HOUGANG', 'HOUGANG'), ('JURONG EAST', 'JURONG EAST'), ('JURONG WEST', 'JURONG WEST'), ('KALLANG/WHAMPOA', 'KALLANG/WHAMPOA'), ('MARINE PARADE', 'MARINE PARADE'), ('PASIR RIS', 'PASIR RIS'), ('PUNGGOL', 'PUNGGOL'), ('QUEENSTOWN', 'QUEENSTOWN'), ('SEMBAWANG', 'SEMBAWANG'), ('SENGKANG', 'SENGKANG'), ('SERANGOON', 'SERANGOON'), ('TAMPINES', 'TAMPINES'), ('TOA PAYOH', 'TOA PAYOH'), ('WOODLANDS', 'WOODLANDS'), ('YISHUN', 'YISHUN')], max_length=512)),
            ],
            managers=[
                ('housingDataMgr', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='ResaleFlatPrice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(max_length=32)),
                ('flatType', models.CharField(max_length=32)),
                ('propertyPrice', models.FloatField()),
            ],
            managers=[
                ('housingCalculateMgr', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='HousingCalculate',
            fields=[
                ('housingUserData', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='House.housinguserdata')),
                ('maxPropertyPrice', models.FloatField()),
                ('downPayment', models.FloatField()),
                ('lumpSumPayment', models.FloatField()),
                ('maxHomeLoan', models.FloatField()),
                ('monthlyInstallment', models.FloatField()),
                ('loanPeriod', models.IntegerField()),
            ],
            managers=[
                ('housingCalculateMgr', django.db.models.manager.Manager()),
            ],
        ),
    ]
