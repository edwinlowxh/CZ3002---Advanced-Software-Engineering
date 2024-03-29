# Generated by Django 3.2.16 on 2023-02-26 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Budget', '0009_budget_budget_budget_limit_range'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='budget',
            name='budget_budget_limit_range',
        ),
        migrations.AddConstraint(
            model_name='budget',
            constraint=models.CheckConstraint(check=models.Q(('limit__gte', 0.0), ('limit__lte', 100000000)), name='budget_budget_limit_range'),
        ),
    ]
