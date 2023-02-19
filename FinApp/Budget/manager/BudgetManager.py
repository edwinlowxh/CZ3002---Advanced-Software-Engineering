from __future__ import annotations

from typing import TYPE_CHECKING

from django.db import models

from django.contrib.auth.models import User 

from django.utils.timezone import datetime

if TYPE_CHECKING:
    from Budget.models import Category
    from Budget.models import Budget 


class BudgetManager(models.Manager):
    def retrieve_budget(self, year, month, **kwargs) -> models.QuerySet:
        user = kwargs['user']

        return super().get_queryset().filter(
            user=user,
            date__year=year,
            date__month = month
        )
    
    def create_budget(self, user: User, limit: float, date: datetime, category: Category) -> Budget:
        return super().create(
            user=user,
            limit = limit,
            date = date,
            category=category
        )

    def delete_budget(self, id: int) -> None:
        super().delete(
            id=id
        )

    def update_budget(self, id: int, user: User, date: datetime, category: Category, limit: float, description: str, type: str) -> Budget:
        return super().update(
            id=id,
            user=user,
            date=date,
            category=category,
            limit=limit
        )