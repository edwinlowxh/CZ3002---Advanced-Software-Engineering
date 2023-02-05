from django.contrib.auth.models import User

from django.utils import timezone

from user_profile.constants import *
from user_profile.models import UserInformation

def save_user_information(user: User, marital_status: str, birth_date: tuple) -> None:
    day, month, year = birth_date

    if UserInformation.objects.filter(user=user).exists():
        user_information = UserInformation.objects.get(user=user)
        user_information.marital_status = marital_status
        user_information.birth_date = timezone.datetime(year=int(year), month=int(month), day=int(day))
    else:
        user_information = UserInformation(
            user=user,
            marital_status=marital_status,
            birth_date=timezone.datetime(year=int(year), month=int(month), day=int(day))
        )

    user_information.save()

def retrieve_user_information(user: User) -> UserInformation:
    if UserInformation.objects.filter(user=user).exists():
        return UserInformation.objects.get(user=user)
    else:
        return None
