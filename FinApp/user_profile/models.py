from django.db import models
from django.contrib.auth.models import User

from user_profile.manager import UserInformationManager

# Create your models here.
class UserInformation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField()
    marital_status = models.CharField(max_length=7)
    user_information_manager = UserInformationManager()

    