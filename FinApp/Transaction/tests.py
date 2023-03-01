import sys

from django.test import TestCase

from django.utils.timezone import datetime

from django.contrib.auth.models import User

from Budget.models import Category
from Transaction.models import Transaction

# Create your tests here.
class TestTransaction(TestCase):
    @classmethod
    def setUp(self):
        self.user=User.objects.create_user(username="testuser", password="testuserpassword", email="testuser@email.com")
        self.category1 = Category.category_manager.create_category(user=self.user, name="Test Category_1")
        self.category2 = Category.category_manager.create_category(user=self.user, name="Test_Category_2")

    def print_fail(self, function_name: str):
        sys.stdout.write('\b')
        print(f'{function_name} [FAILED]')

    def print_pass(self, function_name: str):
        sys.stdout.write('\b')
        print(f'{function_name} [PASSED]')
    
    def test1_create_expense(self):
        new_expense = Transaction.transaction_manager.create_transaction(
            user=self.user,
            category=self.category1,
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

    def test3_update_transaction(self):
        new_income = Transaction.transaction_manager.create_transaction(user=self.user, category=None, amount=10,
            date=datetime.now(), description="test3_update_transaction_income", type='INCOME'
        )

        new_expense = Transaction.transaction_manager.create_transaction(user=self.user, category=self.category1,
            amount=10, date=datetime.now(), description="test3_update_transaction_expense", type='EXPENSE'
        )

        Transaction.transaction_manager.update_transaction(user=self.user, id=new_income.id, category=None,
            amount=100, date=datetime(2022,1,1), description="test3_update_transaction_income_new", type='INCOME'
        )

        Transaction.transaction_manager.update_transaction(user=self.user, id=new_expense.id, category=self.category2,
            amount=100, date=datetime(2022,1,1), description="test3_update_transaction_expense_new", type='EXPENSE'
        )

        transactions = Transaction.transaction_manager.retrieve_transaction(
            user=self.user
        )

        try:
            for transaction in transactions:
                if transaction.id == new_expense.id:
                    self.assertEqual(transaction.amount, 100)
                    self.assertEqual(transaction.category, self.category2)
                    self.assertEqual(transaction.date.year, 2022)
                    self.assertEqual(transaction.date.month, 1)
                    self.assertEqual(transaction.date.day, 1)
                    self.assertEqual(transaction.description, 'test3_update_transaction_expense_new')
                else:
                    self.assertEqual(transaction.amount, 100)
                    self.assertEqual(transaction.date.year, 2022)
                    self.assertEqual(transaction.date.month, 1)
                    self.assertEqual(transaction.date.day, 1)
                    self.assertEqual(transaction.description, 'test3_update_transaction_income_new')
        except Exception as e:
            self.print_fail("test3_update_transaction")
            raise e
        
        Transaction.transaction_manager.delete_transaction(user=self.user, id=new_expense.id)
        Transaction.transaction_manager.delete_transaction(user=self.user, id=new_income.id)
        self.print_pass(function_name='test3_update_transaction')

    def test4_delete_transaction(self):
        Transaction.transaction_manager.create_transaction(user=self.user, category=None,
            amount=10, date=datetime.now(), description="test4_delete_transaction", type='INCOME'
        )
        
        query_set = Transaction.transaction_manager.retrieve_transaction(
            user=self.user
        )

        try:
            self.assertEqual(len(query_set), 1)
        except Exception as e:
            self.print_fail("test4_delete_transaction")
            raise e

        Transaction.transaction_manager.delete_transaction(user=self.user, id=query_set[0].id)

        query_set = Transaction.transaction_manager.retrieve_transaction(
            user=self.user
        )

        try:
            self.assertEqual(len(query_set), 0)
        except Exception as e:
            self.print_fail("test4_delete_transaction")
            raise e

        self.print_pass("test4_delete_transaction") 

    def test5_sum_of_category(self):
        new_expense_1 = Transaction.transaction_manager.create_transaction(user=self.user, category=self.category1,
            amount=9889.23, date=datetime.now(), description="test2_create_income", type='EXPENSE'
        )

        new_expense_2 = Transaction.transaction_manager.create_transaction(user=self.user, category=self.category1,
            amount=2387.23, date=datetime.now(), description="test2_create_income", type='EXPENSE'
        )

        try:
            self.assertEqual(Transaction.transaction_manager.sum_of_category(user=self.user, category=self.category1), 9889.23 + 2387.23)
            self.assertEqual(Transaction.transaction_manager.sum_of_category(user=self.user, category=self.category2), 0)
        except Exception as e:
            self.print_fail('test5_sum_of_category')
            raise e

        Transaction.transaction_manager.delete_transaction(user=self.user, id=new_expense_1.id)
        Transaction.transaction_manager.delete_transaction(user=self.user, id=new_expense_2.id)
        self.print_pass('test5_sum_of_category')







