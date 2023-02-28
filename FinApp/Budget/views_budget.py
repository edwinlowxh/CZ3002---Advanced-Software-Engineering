from django.shortcuts import render

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
    BUDGET_MONTH_VAR
)

from .models import Category, Budget

from .forms.CreateBudgetForm import CreateBudgetForm

# Create your views here.


@csrf_exempt
@basic_auth
def create_budget(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
           
            form_data = CreateBudgetForm.map_json(request.POST.dict())
            form_data['user'] = request.user
            form_data['year'] = request.POST.get(BUDGET_YEAR_VAR)
            form_data['month'] = request.POST.get(BUDGET_MONTH_VAR)
            
            form = CreateBudgetForm(form_data)
            
            if form.is_valid():
                print(form.cleaned_data)
                category = form.cleaned_data["category"]
                year = form.cleaned_data["year"]
                month = form.cleaned_data["month"]
                query_set = Budget.budget_manager.get_budget(category = category, year= year, month = month)
                if query_set:
                    return JsonResponse({"Error": "You cannot create more than one budget for the same category in the same year and month!"})
                else:
                    try: 
                        new_budget = Budget.budget_manager.create_budget(**form.cleaned_data)
                        return JsonResponse(model_to_dict(new_budget))
                    except Exception as e:
                        return JsonResponse({"Message": "Failed to create a budget",
                                             "Error" :  str(e)})
                
            else:
                return JsonResponse({'Message': 'Failed to create budget', 'errors': form.errors})

        elif request.method == 'GET':
            budgets = Budget.budget_manager.get_budget(user = request.user)
            return JsonResponse({'budgets': [model_to_dict(budget) for budget in budgets]})
            

@csrf_exempt
@basic_auth
def delete_budget(request):
     if request.user.is_authenticated:
        if request.method == 'POST':
            budget_id = request.POST.get(BUDGET_ID_VAR)
            try:
                Budget.budget_manager.delete_budget(user=request.user, id=budget_id)
                return JsonResponse({'Message': 'Budget Deleted'})
            
            except Exception as e:                
                return JsonResponse({"Message": "Failed to delete a budget",
                                     "Error" :  str(e)})

@csrf_exempt
@basic_auth
def update_budget(request):
     if request.user.is_authenticated:
        if request.method == 'POST':
            budget_id = request.POST.get(BUDGET_ID_VAR)

            try:
                form_data = CreateBudgetForm.map_json(request.POST.dict())
                form_data['user'] = request.user
                form_data['year'] = request.POST.get(BUDGET_YEAR_VAR)
                form_data['month'] = request.POST.get(BUDGET_MONTH_VAR)
                form = CreateBudgetForm(form_data)
                
                if form.is_valid():
                    print(form.cleaned_data)
                    updated_budget = Budget.budget_manager.update_budget(id = budget_id, **form.cleaned_data)

                    if not updated_budget:
                        return JsonResponse({'message': 'Failed to update budget', 'errors': 'Budget does not exist'})
                    else:
                        return JsonResponse(model_to_dict(updated_budget))
                else:
                    return JsonResponse({'message': 'Failed to update budget', 'errors': form.errors})

            except Exception as e:           
                return JsonResponse({"Message": "Failed to update a budget",
                                     "Error" :  str(e)})
           