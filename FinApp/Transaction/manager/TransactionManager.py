from __future__ import annotations

from typing import TYPE_CHECKING

from django.db import models

from django.contrib.auth.models import User

from django.utils.timezone import datetime

if TYPE_CHECKING:
    from Budget.models import Category
    from Transaction.models import Transaction


class TransactionManager(models.Manager):
    def retrieve_transaction(self, **kwargs) -> models.QuerySet:
        user = kwargs['user']
        
        if 'start_date' not in kwargs:
            start_date = datetime(1900,1,1)
        else:
            start_date = datetime(int(kwargs['start_date'][2]), int(kwargs['start_date'][1]), int(kwargs['start_date'][0]))
            
        if 'end_date' not in kwargs:
            end_date = datetime.now()
        else:
            end_date = datetime(int(kwargs['end_date'][2]), int(kwargs['end_date'][1]), int(kwargs['end_date'][0]))

        return super().get_queryset().filter(
            user=user,
            date__range=(start_date, end_date)
        )
    
    def create_transaction(self, user: User, category: Category, amount: float, description: str, type: str) -> Transaction:
        return super().create(
            user=user,
            category=category,
            amount=amount,
            description=description,
            type=type,
        )

    def delete_transaction(self, id: int) -> None:
        super().delete(
            id=id
        )

    def update_transaction(self, id: int, user: User, date: datetime, category: Category, amount: float, description: str, type: str) -> Transaction:
        return super().update(
            id=id,
            user=user,
            date=date,
            category=category,
            amount=amount,
            description=description,
            type=type,
        )



