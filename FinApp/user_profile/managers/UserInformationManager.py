from django.contrib.auth.models import User

from django.utils.timezone import datetime

from user_profile.constants import *

from django.db import models

class UserInformationManager(models.Manager):
    def retrieve_user_information(self, user: User) -> models.QuerySet:
        return super().get_queryset().filter(user=user)

    def save_user_information(self, user: User, marital_status: str, date_of_birth: datetime) -> None:
        self.retrieve_user_information(user).update_or_create(
            user=user,
            defaults={
                'marital_status': marital_status,
                'date_of_birth': date_of_birth
            }
        )
