from __future__ import annotations

from typing import TYPE_CHECKING

from django.db import models

from django.contrib.auth.models import User 

from django.utils.timezone import datetime

from django.db.models import Sum

if TYPE_CHECKING:
    from Budget.models import Category
    from Budget.models import Budget 


class BudgetManager(models.Manager):
    def get_budget(self,**kwargs) -> models.QuerySet:
        filter_kwargs = {}
        if 'user' in kwargs and kwargs['user']:
            filter_kwargs['user'] = kwargs['user']
        if 'year' in kwargs and kwargs['year']:
            filter_kwargs['year'] = kwargs['year']
        if 'month' in kwargs and kwargs['month']:
            filter_kwargs['month'] = kwargs['month']
        if 'category' in kwargs and kwargs['category']:
            filter_kwargs['category'] = kwargs['category']
        if 'id' in kwargs and kwargs['id']:
            filter_kwargs['id'] = kwargs['id']

        return super().get_queryset().filter(**filter_kwargs)
    
    def get_budget_total(self,user: User, year: int, month:int) -> models.QuerySet:
        return super().get_queryset().filter(user=user, year= year, month = month).aggregate(Sum('limit'))
            
    def create_budget(self, user: User, limit: float, year: int, month: int, category: Category) -> Budget:
        return super().create(
            user = user,
            limit = limit,
            year = year,
            month = month, 
            category=category
        )

    def delete_budget(self, user: User, id: int) -> None:
        super().get_queryset().filter(
            user=user,
            id=id
        ).delete()


    def update_budget(self, user: User, id: int, **kwargs) -> Budget:
        query_set = self.get_budget(user=user, id=id)
        if not query_set:
            return None
        else:
            filter_kwargs = {}
            if 'category' in kwargs and kwargs['category']:
                filter_kwargs['category'] = kwargs['category']
            if 'limit' in kwargs and kwargs['limit']:
                filter_kwargs['limit'] = kwargs['limit']

            query_set.update(**filter_kwargs)
            return query_set[0]
        
