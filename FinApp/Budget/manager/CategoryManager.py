from __future__ import annotations

from typing import TYPE_CHECKING

from django.db import models

from django.contrib.auth.models import User 

from django.utils.timezone import datetime

if TYPE_CHECKING:
    from Budget.models import Category

class CategoryManager(models.Manager):
    def get_categories(self, **kwargs) -> models.QuerySet:
        filter_kwargs = {}
        if 'user' in kwargs and kwargs['user']:
            filter_kwargs['user'] = kwargs['user']
        if 'name' in kwargs and kwargs['name']:
            filter_kwargs['name'] = kwargs['name']
        if 'id' in kwargs and kwargs['id']:
            filter_kwargs['id'] = kwargs['id']
        if 'is_active' in kwargs and kwargs['is_active']:
            filter_kwargs['is_active'] = kwargs['is_active']

        return super().get_queryset().filter(**filter_kwargs)
    
    def create_category(self, user: User, name: str) -> Category:
        category, created = super().update_or_create(
            user = user,
            name = name,
            defaults={'user': user, 'name': name, "is_active": True},
        )
        return category

    def delete_category(self, user: User, id: int) -> None:
        self.get_categories(user = user, id=id).update(is_active = False)
       

    def update_category(self, user: User,  id: int,  name: str) -> Category:
        query_set = self.get_categories(user=user,id=id)
        if not query_set:
            return None
        else:
            query_set.update(name=name)
            return query_set[0]
        
    