from django.db import models
from django.contrib.auth.models import User

from django.utils.timezone import now

from .constants import TRANSACTION_TYPE

from Budget.models import Category

from multiselectfield import MultiSelectField

# Create your models here.

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.CASCADE)
    amount = models.FloatField()
    date = models.DateField(default=now)
    description = models.TextField()
    type = MultiSelectField(choices=TRANSACTION_TYPE)