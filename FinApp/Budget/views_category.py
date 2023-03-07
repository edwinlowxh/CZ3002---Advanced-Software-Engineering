from django.shortcuts import render, redirect

from django.forms import model_to_dict

from django.views.decorators.csrf import csrf_exempt

from django.http import JsonResponse

from django.db import utils

from FinApp.decorators import basic_auth

from .models import Category, Budget

from .constants import(
    CATEGORY_NAME_VAR,
    CATEGORY_ID_VAR,
    CATEGORY_TABLE_HEADER,
)

from .forms.CreateCategoryForm import CreateCategoryForm

# Create your views here.

def get_category(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            context = {'category_table_header': CATEGORY_TABLE_HEADER}   
            query_set = Category.category_manager.get_categories(user = request.user, is_active = True)         
            context['categories'] = [model_to_dict(category) for category in query_set]
            print(request.user, context)
            return render(request, 'categories.html', context)
    else:
        return redirect('/profile/login')

@csrf_exempt
def create_category(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form_data = CreateCategoryForm.map_json(request.POST.dict())
            form_data['user'] = request.user
            form = CreateCategoryForm(update=False, **form_data)
            
            if form.is_valid():
                new_category = Category.category_manager.create_category(
                    **form.cleaned_data
                )
                context = model_to_dict(new_category)
                return JsonResponse(context, status = 201)
                return render(request,"", context)
            else:
                return JsonResponse({'message': 'Failed to create category', 'errors': CreateCategoryForm.map_fields(form.errors, reverse=True)}, status=422)
            
        elif request.method == 'GET':
            context = {'category_table_header': CATEGORY_TABLE_HEADER}  
            query_set = Category.category_manager.get_categories(user = request.user, is_active = True)         
            context['categories'] = [model_to_dict(category) for category in query_set]
            return render(request, "categories.html", context)    
                        
@csrf_exempt
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
           



