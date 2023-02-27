import traceback, sys

from django.test import TestCase

from django.utils.timezone import datetime

from django.contrib.auth.models import User

from Budget.models import Category
from Transaction.models import Transaction

# Create your tests here.
class TestBudgetModels(TestCase):
    @classmethod
    def setUp(self):
        self.user=User.objects.create_user(username="testuser", password="testuserpassword", email="testuser@email.com")
        self.category = Category.category_manager.create_category(user=self.user, name="Food")

    def print_fail(self, function_name: str):
        sys.stdout.write('\b')
        print(f'{function_name} [FAILED]')

    def print_pass(self, function_name: str):
        sys.stdout.write('\b')
        print(f'{function_name} [PASSED]')
    
    def test1_create_expense(self):
        new_expense = Transaction.transaction_manager.create_transaction(
            user=self.user,
            category=self.category,
            amount=10,
            date=datetime.now(),
            description="test1_create_expense",
            type='EXPENSE'
        )

        query_set = Transaction.transaction_manager.retrieve_transaction(
            user=self.user
        )

        try:
            self.assertEqual(len(query_set), 1)
            self.assertEqual(query_set[0], new_expense)
        except Exception as e:
            self.print_fail("test1_create_expense")
            raise e

        Transaction.transaction_manager.delete_transaction(
            user=self.user,
            id=query_set[0].id
        )
        self.print_pass("test1_create_expense")
        

    def test2_create_income(self):
        new_income = Transaction.transaction_manager.create_transaction(
            user=self.user,
            category=None,
            amount=10,
            date=datetime.now(),
            description="test2_create_income",
            type='INCOME'
        )

        query_set = Transaction.transaction_manager.retrieve_transaction(
            user=self.user
        )

        try:
            self.assertEqual(len(query_set), 1)
            self.assertEqual(query_set[0], new_income)
        except Exception as e:
            self.print_fail("test2_create_income")
            raise e
            
        Transaction.transaction_manager.delete_transaction(
            user=self.user,
            id=query_set[0].id
        )
        self.print_pass("test2_create_income")


