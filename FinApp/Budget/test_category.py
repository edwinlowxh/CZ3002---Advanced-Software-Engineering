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

    def test0_get_category(self):
         #Getting ALL categories 
         catergories = Category.category_manager.get_categories(user=self.user)
         cat_list = [cat.name for cat in catergories]
         print(cat_list)

         #Getting one category based on name
         catergories = Category.category_manager.get_categories(user=self.user, name = "Rent")  
         cat_list = [cat.name for cat in catergories]
         print(cat_list)

         #Getting one category based on ID
         catergories = Category.category_manager.get_categories(user=self.user, id = 1)  
         cat_list = [cat.name for cat in catergories]
         print(cat_list)


    def test1_update_category(self):
         updated_cat = Category.category_manager.update_category(user = self.user, id=1, name= "UPDATED CATEGORY NAME")
         print(updated_cat.name)


    def test2_delete_category(self):
        catergories = Category.category_manager.get_categories(user=self.user)
        print("Category: " + catergories[0].name + "|| Status " +  str(catergories[0].is_active))
        Category.category_manager.delete_category(user = self.user, id=1)
        print("Category: " + catergories[0].name + "|| Status " +  str(catergories[0].is_active))


    def test3_model_str(self):
        cat_name = Category.category_manager.create_category(user=self.user,name = "Django Test Category")
        self.assertEqual(str(cat_name), "Django Test Category")
        

    
    def test4_duplicate_cat(self):
        try:
            cat_name = Category.category_manager.create_category(user=self.user,name = "Django Test Category")
            cat_name = Category.category_manager.create_category(user=self.user,name = "Django Test Category")
        except IntegrityError as e: 
            print(e)

