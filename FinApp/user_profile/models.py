from django.db import models
from django.contrib.auth.models import User

from user_profile.managers.UserInformationManager import UserInformationManager

# Create your models here.
class UserInformation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    marital_status = models.CharField(null=True, max_length=7)
    user_information_manager = UserInformationManager()

    