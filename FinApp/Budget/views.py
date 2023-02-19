from django.shortcuts import render

from django.forms import model_to_dict

from django.views.decorators.csrf import csrf_exempt

from django.http import JsonResponse

from django.db import utils

from FinApp.decorators import basic_auth

from .models import Category, Budget

from .constants import(
    CATEGORY_NAME_VAR
)

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

            
            



