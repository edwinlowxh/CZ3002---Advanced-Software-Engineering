from django.shortcuts import render

from django.forms import model_to_dict

from django.views.decorators.csrf import csrf_exempt

from django.http import JsonResponse

from django.db import utils

from FinApp.decorators import basic_auth

from .models import Category, Budget

from .constants import(
    CATEGORY_NAME_VAR,
    CATEGORY_ID_VAR

)

from .forms.CreateCategoryForm import CreateCategoryForm

# Create your views here.

@csrf_exempt
@basic_auth
def create_category(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            category_name = request.POST.get(CATEGORY_NAME_VAR, default=None)
            if category_name:
                try:
                    new_category = Category.category_manager.create_category(user=request.user, name=request.POST[CATEGORY_NAME_VAR])
                    return JsonResponse(data=model_to_dict(new_category))
                except utils.IntegrityError:
                    return JsonResponse(data={'message': 'Category exists'})
            else:
                return JsonResponse(data={'message': 'Please provide a name for your category'})

@csrf_exempt
@basic_auth
def create_category(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form_data = CreateCategoryForm.map_json(request.POST.dict())
            form_data['user'] = request.user
            form = CreateCategoryForm(update=False, **form_data)
            
            if form.is_valid():
                print(form.cleaned_data)
                new_category = Category.category_manager.create_category(
                    **form.cleaned_data
                )
                return JsonResponse(model_to_dict(new_category))
            else:
                return JsonResponse({'message': 'Failed to create category', 'errors': form.errors})

            # except Exception as e:
            #     return JsonResponse({'message': 'Failed to create new transaction'})
        elif request.method == 'GET':
            categories = Category.category_manager.get_categories(user=request.user, is_active = True)
            return JsonResponse({'categories': [model_to_dict(category) for category in categories]})
            

@csrf_exempt
@basic_auth
def delete_category(request):
     if request.user.is_authenticated:
        if request.method == 'POST':
            category_id = request.POST.get(CATEGORY_ID_VAR)
            try:
                Category.category_manager.delete_category(user=request.user, id=category_id)
                return JsonResponse({'message': 'Category Deleted'})
            except Exception as e:                
                return JsonResponse({'message': 'Failed to delete category'})

@csrf_exempt
@basic_auth
def update_category(request):
     if request.user.is_authenticated:
        if request.method == 'POST':
            category_id = request.POST.get(CATEGORY_ID_VAR)

            try:
                form_data = CreateCategoryForm.map_json(request.POST.dict())
                form_data['user'] = request.user
                form = CreateCategoryForm(update=True, **form_data)
                
                if form.is_valid():
                    print(form.cleaned_data)
                    updated_category =  Category.category_manager.update_category(
                        id=category_id,
                        **form.cleaned_data
                    )

                    if not updated_category:
                        return JsonResponse({'message': 'Failed to update category', 'errors': 'Category does not exist'})
                    else:
                        return JsonResponse(model_to_dict(updated_category))
                else:
                    return JsonResponse({'message': 'Failed to update category', 'errors': form.errors})

            except Exception as e:           
                return JsonResponse({'message': 'Failed to update category'})
           



