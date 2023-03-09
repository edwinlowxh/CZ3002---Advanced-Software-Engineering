from django.forms import model_to_dict
from django.shortcuts import redirect, render

from .models import Transaction

from .form.CreateTransactionForm import CreateTransactionForm

from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt

from FinApp.decorators import basic_auth

import json 

from django.core import serializers

from .constants import (
    START_DATE_QUERY_PARAM,
    END_DATE_QUERY_PARAM,
    TRANSACTION_ID_VAR,
    INCOME_TABLE_HEADER,
    EXPENSE_TABLE_HEADER
)

from Budget.models import(
    Category
)

# Create your views here.
@csrf_exempt
# @basic_auth
def get_transactions(request, start_date: str = None, end_date: str = None):
    if request.user.is_authenticated:
        if request.method == 'GET':
            start_date = request.GET.get(START_DATE_QUERY_PARAM, None)
            end_date = request.GET.get(END_DATE_QUERY_PARAM, None)
            context = {'income_table_header': INCOME_TABLE_HEADER, 'expense_table_header': EXPENSE_TABLE_HEADER}            

            if not start_date and not end_date:
                query_set = Transaction.transaction_manager.retrieve_transaction(user=request.user)
                context['range'] = 'Any'
                # return JsonResponse({'range': 'Any', 'transactions': [model_to_dict(transaction) for transaction in query_set]})
            elif not start_date:
                query_set = Transaction.transaction_manager.retrieve_transaction(user=request.user, end_date=tuple(end_date.split('-')))
                context['range'] = f'Before {end_date}'
                # return JsonResponse({'range': f'Before {end_date}', 'transactions': [model_to_dict(transaction) for transaction in query_set]})
            elif not end_date:
                query_set = Transaction.transaction_manager.retrieve_transaction(user=request.user, start_date=tuple(start_date.split('-')))
                context['range'] = f'After {start_date}'
                # return JsonResponse({'range': f'After {start_date}', 'transactions': [model_to_dict(transaction) for transaction in query_set]})
            else:
                query_set = Transaction.transaction_manager.retrieve_transaction(user=request.user, start_date=tuple(start_date.split('-')), end_date=tuple(end_date.split('-')))
                context['range'] = f'From {start_date} to {end_date}'
                # return JsonResponse({'range': f'From {start_date} to {end_date}', 'transactions': [model_to_dict(transaction) for transaction in query_set]})
                
            serialized_data = json.loads(serializers.serialize('json', query_set, use_natural_foreign_keys=True, use_natural_primary_keys=True))
            for data in serialized_data:
                transaction = data["fields"]
                del transaction["user"]
                transaction.update({"id": data["pk"]})

            context['transactions'] = [data["fields"] for data in serialized_data]
            #context['transactions'] = [model_to_dict(transaction) for transaction in query_set]
            print(request.user, context)
            return render(request, 'transaction.html', context)
    else:
        return redirect('/login')

@csrf_exempt
@basic_auth
def create_transaction(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form_data = CreateTransactionForm.map_fields(request.POST.dict())
            form = CreateTransactionForm(request.user, **form_data)

            if form.is_valid():
                print(form.cleaned_data)
                new_transaction = Transaction.transaction_manager.create_transaction(
                    user=request.user,
                    **form.cleaned_data
                )
                context = model_to_dict(new_transaction)
                return JsonResponse(context, status=201)
            else:
                return JsonResponse({'message': 'Failed to create transaction', 'field_errors': CreateTransactionForm.map_fields(form.errors, reverse=True)}, status=422)
        elif request.method == 'GET':
            categories = Category.category_manager.get_categories(user=request.user)
            context = {'categories': [model_to_dict(category)['name'] for category in categories]}
            print(context)
            return JsonResponse(context)

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
                form_data = CreateTransactionForm.map_fields(request.POST.dict())
                form = CreateTransactionForm(request.user, form_data)

                if form.is_valid():
                    updated_transaction = Transaction.transaction_manager.update_transaction(
                        user=request.user,
                        id=transaction_id,
                        **form.cleaned_data
                    )

                    if not updated_transaction:
                        return JsonResponse({'message': 'Failed to update transaction', 'errors': 'Transaction do not exist'})
                    else:
                        return JsonResponse(model_to_dict(updated_transaction))
                else:
                    return JsonResponse({'message': 'Failed to update transaction', 'errors': CreateTransactionForm.map_fields(form.errors, reverse=True)})

            except Exception as e:           
                return JsonResponse({'message': 'Failed to update transaction'})
            
        elif request.method == 'GET':
            transaction_id = request.POST.get(TRANSACTION_ID_VAR)
            transaction = Transaction.transaction_manager.retrieve_transaction(user=request.user, id=transaction_id)
            context = {model_to_dict(transaction)}
            return JsonResponse(context)
            return render(request, "", context)


            



            



            


