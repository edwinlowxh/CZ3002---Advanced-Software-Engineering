from django.db import models

from django.contrib.auth.models import User

from django.utils.timezone import now

# Create your models here.
class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    limit = models.FloatField()
    date = models.DateField(default=now)
    category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.CASCADE)
    
