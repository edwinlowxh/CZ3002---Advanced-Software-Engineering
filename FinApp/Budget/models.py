from django.db import models

from django.db.models import Q

from django.contrib.auth.models import User

from django.utils.timezone import now

from .manager.CategoryManager import CategoryManager

from .manager.BudgetManager import BudgetManager

# Create your models here.
class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    category_manager = CategoryManager()
    
    def __str__(self):
        return self.name
    
    def natural_key(self):
        return (self.name)
        
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'name'], name='unique_user_category'),
        ]

class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    limit = models.FloatField()
    #date = models.DateField(default=now)
    year = models.PositiveIntegerField()
    month = models.PositiveIntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    budget_manager = BudgetManager()
    
    def __str__(self):
        return self.category.name
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'category' , 'year', 'month'], name='unique_user_budget_by_date'),
            models.CheckConstraint(name="%(app_label)s_%(class)s_year_range", check=models.Q(year__range=(1990, 2100))),
            models.CheckConstraint(name="%(app_label)s_%(class)s_month_range", check=models.Q(month__range=(1, 12))),
            models.CheckConstraint(name="%(app_label)s_%(class)s_limit_range", check = Q(limit__gte=0.0) & Q(limit__lte=100000000))       
            ]
    
