from django.shortcuts import redirect, render

from django.views.decorators.csrf import csrf_exempt

from FinApp.decorators import basic_auth

from django.db import utils

from .models import Budget

from Transaction.models import Transaction

import datetime

@csrf_exempt
@basic_auth
def get_budget_home(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
    
            user = request.user
            today = datetime.date.today()
            year = today.year
            month = today.month

            context = {}
            context["total_budget_limit"] = (Budget.budget_manager.get_budget_total(user = user, year = year, month = month)["limit__sum"] or 0)
            context["total_spent"] = (Transaction.transaction_manager.retrieve_total_expenses(user = user, year = year, month = month)["amount__sum"] or 0)
        
            budgets = Budget.budget_manager.get_budget(user = user, year = year, month = month)
            budget_list = []
            
            colour_array = ["#d24747","#439a50","#a11adb","#4148d4","#ce8551","#df3eb1"]
            colour_array_lighter = ["#be7b7b","#83b890","#9f91a7","#7f86a3","#d0b48e","#d19bc7"]

            for budget in budgets:
                budget_dict = {}
                budget_dict["name"] = budget.category.name
                budget_dict["spent"] = (Transaction.transaction_manager.retrieve_total_expenses(user=user, year = year, month=month, category = budget.category)["amount__sum"] or 0)
                budget_dict["limit"] = budget.limit
                budget_dict["percentage"] = (budget_dict["spent"] / budget_dict["limit"] / context["total_budget_limit"]) * 100
                budget_dict["individual"] = (budget_dict["spent"] / budget_dict["limit"]) * 100
                budget_dict["color"] = colour_array.pop(0)
                budget_dict["color_gradient"] = "linear-gradient(to top," + budget_dict["color"] + "," + colour_array_lighter.pop(0) +")"
                budget_list.append(budget_dict)

                   
            context["budgets"] = budget_list
            print(request.user, context)
            return render(request, 'home.html', context)


    else:
        return redirect('/profile/login')

        
           