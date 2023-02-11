from django.contrib.auth.models import User

from django.utils import timezone

from user_profile.constants import *

from django.db import models
from django.db.models import QuerySet

class UserInformationManager(models.Manager):
    def retrieve_user_information(self, user: User) -> QuerySet:
        return super().get_queryset().filter(user=user)

    def save_user_information(self, user: User, marital_status: str, birth_date: tuple) -> None:
        day, month, year = birth_date

        self.retrieve_user_information(user).update_or_create(
            user=user,
            defaults={
                'marital_status': marital_status,
                'birth_date': timezone.datetime(year=int(year), month=int(month), day=int(day))
            }
        )
