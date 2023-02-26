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

        #Creating a budget for all catergories 
        catergories = Category.category_manager.get_categories(user=self.user)
        cat_list = [cat for cat in catergories]
        for cat in cat_list:
            new_budget = Budget.budget_manager.create_budget(user = self.user, limit = 200, year = 2023, month = 3, category=cat)
            new_budget.save()

    # def test0_creating_budget(self):
    #      #Getting ALL categories 
    #      catergories = Category.category_manager.get_categories(user=self.user)
    #      cat_list = [cat for cat in catergories]
    #      print(cat_list)
         
    #      #Creating a budget for all catergories 
    #      for cat in cat_list:
    #          new_budget = Budget.budget_manager.create_budget(user = self.user, limit = 200, year = 2023, month = 3, category=cat)
    #          new_budget.save()
    
    def test1_getting_budget(self):
         print("*"*30 + " TEST CASE 1: GET methods of Budget Manager " + "*"*30)
         
         print("Scenario 1: Getting all budgets of a user based on the year and month")
         budgets = Budget.budget_manager.get_budget(user = self.user, year = 2023, month = 3)
         budget_by_year_month = [budget for budget in budgets]
         print(budget_by_year_month)
         print()
         

         print("Getting specific budget based on year, month and category")
         rent_category = Category.category_manager.get_categories(user=self.user, name = "Rent")[0]
         budgets = Budget.budget_manager.get_budget(user = self.user, year=2023, month = 3, category = rent_category)
         budget_list = [(budget.category.name,budget.limit) for budget in budgets]
         print(budget_list)
         print()

         print("Getting specific budget based on unique ID")
         budgets = Budget.budget_manager.get_budget(user = self.user, id=1)
         budget_list = [(budget.id,budget.category.name,budget.limit) for budget in budgets]
         print(budget_list)
         print()

    
    def test2_update_budget(self):
        print("*"*30 + " TEST CASE 2: UPDATE methods of Budget Manager " + "*"*30)
        
        #update year and limit
        Budget.budget_manager.update_budget(user = self.user, id=3, year=2024,limit=2000)
        budgets = Budget.budget_manager.get_budget(user = self.user, year = 2023, month = 3)
        budget_by_year_month = [(budget.id,budget.category.name,budget.year, budget.limit) for budget in budgets]
        print(budget_by_year_month)
        budgets = Budget.budget_manager.get_budget(user = self.user, year = 2024, month = 3)
        budget_by_year_month = [(budget.id,budget.category.name,budget.year, budget.limit) for budget in budgets]
        print(budget_by_year_month)
        print()


    
    def test3_delete_budget(self):

        print("*"*30 + " TEST CASE 3: DELETE methods of Budget Manager " + "*"*30)
        
        food_cat = Category.category_manager.get_categories(user=self.user, name = "Food")[0]
        food_budget = Budget.budget_manager.get_budget(user = self.user, category = food_cat)[0]
        print("Budget for " + food_budget.category.name + " with ID = ", str(food_budget.id) + " is present -- " + str(food_budget))

        #Delete a budget
        Budget.budget_manager.delete_budget(user = self.user, id=food_budget.id)
        food_budget = Budget.budget_manager.get_budget(user = self.user, category = food_cat)
        if (food_budget):
            print("Deletion Unsuccessful")
        else:
            print("Deletion Successful")

        print()
    
    def test4_duplicate_budget(self):
        print("*"*30 + " TEST CASE 4: Duplicate Budgets in the same year and month with the same category " + "*"*30)
        try:
            new_budget = Budget.budget_manager.create_budget(user = self.user, 
                                                             limit = 100, 
                                                             year = 2023, 
                                                             month = 3, 
                                                             category= Category.category_manager.get_categories(user = self.user,name = "Rent")[0])
        except IntegrityError as e: 
            print(e)

        print()
     

    def test5_year_month_validity(self):
        print("*"*30 + " TEST CASE 5: Out of range values for year and month" + "*"*30)
        try:
            new_cat = Category.category_manager.create_category(user=self.user,name = "Django Test Category")
            new_budget = Budget.budget_manager.create_budget(user = self.user, 
                                                                limit = 100, 
                                                                year = 2002, 
                                                                month = 13, 
                                                                category= new_cat)
        except Exception as e: 
            print(e)

        print()

    def test6_limit_validity(self):
        print("*"*30 + " TEST CASE 6: Negative Values for limit" + "*"*30)
        try:
            new_cat = Category.category_manager.create_category(user=self.user,name = "Django Test Category")
            new_budget = Budget.budget_manager.create_budget(user = self.user, 
                                                                limit = -100, 
                                                                year = 2002, 
                                                                month = 12, 
                                                                category= new_cat)
        except Exception as e: 
            print(e)

        print()