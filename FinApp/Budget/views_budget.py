import json
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

from .forms.CreateBudgetForm import CreateBudgetForm

from django.core import serializers


# Create your views here.
@csrf_exempt
@basic_auth
def budget_view(request):
    if request.user.is_authenticated:
        return render(request, 'budget.html')
    else:
        return redirect('login')
        
@csrf_exempt
@basic_auth
def get_budget(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            year = request.POST.get(BUDGET_YEAR_VAR)
            month = request.POST.get(BUDGET_MONTH_VAR)
                
            user = request.user
            context = {'budget_table_header': BUDGET_TABLE_HEADER}
            categories = Category.category_manager.get_categories(user = user, is_active = True)
            
            category_list = []
            for category in categories:
                category_dict = model_to_dict(category)
                category_dict["category"] = category.name
                query = Budget.budget_manager.get_budget(user=user, category = category, year = year, month = month)

                if query:
                    category_dict["limit"] = query[0].limit
                else:
                    category_dict["limit"] = 0

                category_list.append(category_dict)

            context['budgets'] =  category_list

            print(request.user, context)
            return JsonResponse(context, status=201)
        

@csrf_exempt
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
                        context = model_to_dict(new_budget)
                        return JsonResponse(context, status=201)
                    except Exception as e:
                        return JsonResponse({"Message": "Failed to create a budget",
                                             "Error" :  str(e)})
                
            else:
                return JsonResponse({'Message': 'Failed to create budget', 'errors': CreateBudgetForm.map_fields(form.errors, reverse=True)})

        elif request.method == 'GET':
            query_set = Budget.budget_manager.get_budget(user = request.user)
            context = {'budget_table_header': BUDGET_TABLE_HEADER}
            context["budgets"] = [model_to_dict(budget) for budget in query_set]
            return render(request, 'budget.html', context)
            
            

@csrf_exempt
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
def update_budget(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            try:
                form_data = CreateBudgetForm.map_fields(request.POST.dict(), reverse=False)
                form_data['user'] = request.user
                form = CreateBudgetForm(form_data)
                
                if form.is_valid():
                    updated_budget = Budget.budget_manager.update_budget(**form.cleaned_data)

                    if not updated_budget:
                        updated_budget = Budget.budget_manager.create_budget(**form.cleaned_data)

                    context = {'id': updated_budget.category.id}
                    serialized_data = json.loads(serializers.serialize('json', [updated_budget], use_natural_foreign_keys=True, use_natural_primary_keys=True))[0]
                    context.update(serialized_data['fields'])
                    return JsonResponse(context, status=201)
                else:
                    print(form.errors)
                    return JsonResponse({'message': 'Failed to update budget', 'field_errors': CreateBudgetForm.map_fields(form.errors, reverse=True)}, status=422)

            except Exception as e:           
                return JsonResponse({"Message": "Failed to update a budget",
                                     "non_field_errors" :  str(e)}, status=500)

           