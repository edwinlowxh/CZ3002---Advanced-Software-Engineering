from django.shortcuts import redirect, render

from django.forms import model_to_dict

from django.views.decorators.csrf import csrf_exempt

from django.http import JsonResponse

from django.db import utils

from FinApp.decorators import basic_auth

from .constants import(
    CATEGORY_NAME_VAR,
    CATEGORY_ID_VAR,
    BUDGET_ID_VAR,
    BUDGET_LIMIT_VAR,
    BUDGET_YEAR_VAR,
    BUDGET_MONTH_VAR,
    BUDGET_TABLE_HEADER
)

from .models import Category, Budget
from Transaction.models import(
    Transaction
)

from .forms.CreateBudgetForm import CreateBudgetForm

# Create your views here.
@csrf_exempt
@basic_auth
def get_budget_home(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
    
            user = request.user
            year = 2023 #request.GET.get(BUDGET_YEAR_VAR)
            month = 1 #request.GET.get(BUDGET_MONTH_VAR)

            context = {}
            context["total_budget_limit"] = Budget.budget_manager.get_budget_total(user = user, year = year, month = month)["limit__sum"]
            context["total_spent"] = Transaction.transaction_manager.retrieve_total_expenses(user = user, year = year, month = month)["amount__sum"]
        
            
            budgets = Budget.budget_manager.get_budget(user = user, year = year, month = month)
            budget_list = []
            if budgets:
                for budget in budgets:
                    budget_dict = model_to_dict(budget)
                    total_spent = Transaction.transaction_manager.retrieve_total_expenses(user = user, year = year, month = month, category = budget.category)["amount__sum"]
                    budget_dict["spent"] = total_spent
                    budget_list.append(budget_dict)
            context["budgets"] = budget_list
            
            print(request.user, context)
            return JsonResponse(context)

    else:
        return redirect('/profile/login')
        

           