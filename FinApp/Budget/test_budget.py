from django.test import TestCase
from Budget.models import Category
from Budget.models import Budget
from django.contrib.auth.models import User
from django.db import IntegrityError

# Create your tests here.
class TestBudgetModels(TestCase):

    @classmethod
    def setUp(self):
        self.user=User(username="renhwa", password="password", email="renhwa@test.com")
        self.user.save()

        #Creating 4 new categories 
        categories = ["Food", "Transportation", "Rent", "Health"]
        for cat in categories:
            new_cat = Category.category_manager.create_category(user=self.user, name = cat)
            new_cat.save()