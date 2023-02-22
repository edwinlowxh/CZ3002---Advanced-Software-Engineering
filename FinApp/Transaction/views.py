from django.forms import model_to_dict
from django.shortcuts import render

from .models import Transaction

from .form.CreateTransactionForm import CreateTransactionForm

from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt

from FinApp.decorators import basic_auth

import json

from .constants import (
    START_DATE_QUERY_PARAM,
    END_DATE_QUERY_PARAM,
    TRANSACTION_ID_VAR,
)

from Budget.models import(
    Category
)

# Create your views here.
@csrf_exempt
@basic_auth
def get_transactions(request, start_date: str = None, end_date: str = None):
    if request.user.is_authenticated:
        if request.method == 'GET':
            start_date = request.GET.get(START_DATE_QUERY_PARAM, None)
            end_date = request.GET.get(END_DATE_QUERY_PARAM, None)            

            if not start_date and not end_date:
                query_set = Transaction.transaction_manager.retrieve_transaction(user=request.user)
                return JsonResponse({'range': 'Any', 'transactions': [model_to_dict(transaction) for transaction in query_set]})
            elif not start_date:
                query_set = Transaction.transaction_manager.retrieve_transaction(user=request.user, end_date=tuple(end_date.split('-')))
                return JsonResponse({'range': f'Before {end_date}', 'transactions': [model_to_dict(transaction) for transaction in query_set]})
            elif not end_date:
                query_set = Transaction.transaction_manager.retrieve_transaction(user=request.user, start_date=tuple(start_date.split('-')))
                return JsonResponse({'range': f'After {start_date}', 'transactions': [model_to_dict(transaction) for transaction in query_set]})
            else:
                query_set = Transaction.transaction_manager.retrieve_transaction(user=request.user, start_date=tuple(start_date.split('-')), end_date=tuple(end_date.split('-')))
                return JsonResponse({'range': f'From {start_date} to {end_date}', 'transactions': [model_to_dict(transaction) for transaction in query_set]})

@csrf_exempt
@basic_auth
def create_transaction(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            # try:
            form_data = CreateTransactionForm.map_json(request.POST.dict())
            form_data['user'] = request.user
            form = CreateTransactionForm(form_data)

            if form.is_valid():
                print(form.cleaned_data)
                new_transaction = Transaction.transaction_manager.create_transaction(
                    **form.cleaned_data
                )
                return JsonResponse(model_to_dict(new_transaction))
            else:
                return JsonResponse({'message': 'Failed to create transaction', 'errors': form.errors})

            # except Exception as e:
            #     return JsonResponse({'message': 'Failed to create new transaction'})
        elif request.method == 'GET':
            categories = Category.category_manager.retrieve_category(user=request.user)
            return JsonResponse({'categories': [model_to_dict(category) for category in categories]})

@csrf_exempt
@basic_auth
def delete_transaction(request):
     if request.user.is_authenticated:
        if request.method == 'POST':
            id = request.POST.get(TRANSACTION_ID_VAR)

            try:
                Transaction.transaction_manager.delete_transaction(user=request.user, id=id)
                return JsonResponse({'message': 'Transaction deleted'})
            except Exception as e:                
                return JsonResponse({'message': 'Failed to delete transaction'})

@csrf_exempt
@basic_auth
def update_transaction(request):
     if request.user.is_authenticated:
        if request.method == 'POST':
            transaction_id = request.POST.get(TRANSACTION_ID_VAR)

            try:
                form_data = CreateTransactionForm.map_json(request.POST.dict())
                form_data['user'] = request.user
                form = CreateTransactionForm(form_data)
                

                if form.is_valid():
                    print(form.cleaned_data)
                    updated_transaction = Transaction.transaction_manager.update_transaction(
                        id=transaction_id,
                        **form.cleaned_data
                    )

                    if not updated_transaction:
                        return JsonResponse({'message': 'Failed to update transaction', 'errors': 'Transaction do not exist'})
                    else:
                        return JsonResponse(model_to_dict(updated_transaction))
                else:
                    return JsonResponse({'message': 'Failed to update transaction', 'errors': form.errors})

            except Exception as e:           
                return JsonResponse({'message': 'Failed to update transaction'})


            



            



            


