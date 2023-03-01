from __future__ import annotations

from typing import TYPE_CHECKING

from django.db import models

from django.contrib.auth.models import User

from django.utils.timezone import datetime

if TYPE_CHECKING:
    from Budget.models import Category
    from Transaction.models import Transaction


class TransactionManager(models.Manager):
    def retrieve_transaction(self, user: User, **kwargs) -> models.QuerySet:
        
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
    
    def create_transaction(self, user: User, category: Category, amount: float, description: str, type: str, date: datetime) -> Transaction:
        return super().create(
            user=user,
            category=category,
            amount=amount,
            description=description,
            date=date,
            type=type,
        )

    def delete_transaction(self, user: User, id: int) -> None:
        super().get_queryset().filter(
            user=user,
            id=id
        ).delete()

    def update_transaction(self, id: int, user: User, date: datetime, category: Category, amount: float, description: str, type: str) -> Transaction:
        query_set = self.get_queryset().filter(user=user, id=id)
        
        if not query_set:
            return None
        else:
            query_set.update(
                date=date,
                category=category,
                amount=amount,
                description=description,
                type=type
            )

            return query_set[0]
        
    def sum_of_category(self, user: User, category: Category, **kwargs) -> float:
        query_set = self.retrieve_transaction(user, **kwargs).filter(category=category)

        if not query_set:
            return 0
        else:
            return list(query_set.aggregate(models.Sum('amount')).values())[0]



