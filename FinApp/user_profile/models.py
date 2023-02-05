from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserInformation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    birth_date = models.DateField()
    marital_status = models.CharField(max_length=7)

    