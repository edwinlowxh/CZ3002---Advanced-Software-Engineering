from __future__ import annotations

from typing import TYPE_CHECKING

from django.db import models

from django.contrib.auth.models import User 

from django.utils.timezone import datetime

if TYPE_CHECKING:
    from Budget.models import Category

class CategoryManager(models.Manager):
    def retrieve_category(self, **kwargs) -> models.QuerySet:
        user = kwargs['user']

        return super().get_queryset().filter(
            user=user
        )
    
    def create_category(self, user: User, name: str) -> Category:
        return super().create(
            user=user,
            name = name
        )

    def delete_category(self, id: int) -> None:
        super().update(is_active = False)
        

    def update_category(self, id: int, user: User, name: str, is_active: bool) -> Category:
        return super().update(
            id=id,
            user=user,
            name = name,
            is_active = is_active
        )