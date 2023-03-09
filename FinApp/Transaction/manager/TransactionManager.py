from __future__ import annotations

from typing import TYPE_CHECKING

from django.db import models

from django.contrib.auth.models import User

from django.utils.timezone import datetime

from django.db.models import Sum

import calendar


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
    
    def retrieve_total_expenses(self,user: User, year: int, month:int, **kwargs)-> models.QuerySet:
        filter_kwargs = {}
        filter_kwargs['user'] = user

        start_date = datetime(year,month,1)
        
        end_date = datetime(year,month,calendar.monthrange(year, month)[1])
        filter_kwargs["date__range"] = (start_date, end_date)

        if 'category' in kwargs and kwargs['category']:
            filter_kwargs['category'] = kwargs['category']

        return super().get_queryset().filter(
           **filter_kwargs
        ).aggregate(Sum('amount'))
    
    def retrieve_top_budget(self, user: User, year: int, month:int)-> models.QuerySet:
        start_date = datetime(year,month,1)        
        end_date = datetime(year,month,calendar.monthrange(year, month)[1])
        return super().get_queryset().filter(
            user=user,
            date__range=(start_date, end_date)
        ).values('category').annotate(total = Sum('amount')).order_by('-amount')

    
    
    def create_transaction(self, user: User, amount: float, description: str, type: str, date: datetime, category: Category = None) -> Transaction:
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



