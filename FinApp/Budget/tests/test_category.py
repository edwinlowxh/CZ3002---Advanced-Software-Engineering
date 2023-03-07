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
         print("*"*30 + " TEST CASE 1: GET methods of Category Manager " + "*"*30)

         print("Scenario 1: Getting all catergories of a user")
         catergories = Category.category_manager.get_categories(user=self.user)
         cat_list = [cat.name for cat in catergories]
         print(cat_list)
         print()

         print("Scenario 2: Getting a specific catergory based on name")
         catergories = Category.category_manager.get_categories(user=self.user, name = "Rent")  
         cat_list = [cat.name for cat in catergories]
         print(cat_list)

         print("Scenario 3: Getting a specific catergory based on ID")
         catergories = Category.category_manager.get_categories(user=self.user, id = 1)  
         cat_list = [(cat.name,cat.id) for cat in catergories]
         print(cat_list)
         print()


    def test1_update_category(self):
         print("*"*30 + " TEST CASE 2: UPDATE methods of Category Manager " + "*"*30)

         #update name ONLY
         updated_cat = Category.category_manager.update_category(user = self.user, id=1, name= "UPDATED CATEGORY NAME")
         print(updated_cat.name)
         print()


    def test2_delete_category(self):
        print("*"*30 + " TEST CASE 3: Delete method of Category Manager " + "*"*30)

        catergories = Category.category_manager.get_categories(user=self.user, id = 1)  
        cat_list = [(cat.name,cat.id, cat.is_active) for cat in catergories]
        print(cat_list)

        #Delete first element
        Category.category_manager.delete_category(user = self.user, id=1)
        catergories = Category.category_manager.get_categories(user=self.user, id = 1)  
        cat_list = [(cat.name,cat.id, cat.is_active) for cat in catergories]
        print(cat_list)

        print()
        
    def test3_duplicate_cat(self):
        print("*"*30 + " TEST CASE 4: Creating Duplicate Categories " + "*"*30)
        try:
            cat_name = Category.category_manager.create_category(user=self.user,name = "Django Test Category")
            cat_name = Category.category_manager.create_category(user=self.user,name = "Django Test Category")
        except IntegrityError as e: 
            print(e)

        print()

    def test4_model_str(self):
        cat_name = Category.category_manager.create_category(user=self.user,name = "Django Test Category")
        self.assertEqual(str(cat_name), "Django Test Category")
        

    
   

