from django.forms import model_to_dict
from django.shortcuts import render

from .models import Transaction

from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt

from FinApp.decorators import basic_auth

from .constants import (
    START_DATE_QUERY_PARAM,
    END_DATE_QUERY_PARAM,
    TRANSACTION_AMOUNT_VAR,
    TRANSACTION_DATE_VAR,
    TRANSACTION_TYPE_VAR,
    TRANSCATION_DESCRIPTION_VAR
)

from Budget.constants import(
    CATEGORY_NAME_VAR
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
            category_name = request.POST.get(CATEGORY_NAME_VAR, default=None)
            amount = request.POST.get(TRANSACTION_AMOUNT_VAR, default=0)
            date = request.POST.get(TRANSACTION_DATE_VAR, default=None)
            description = request.POST.get(TRANSCATION_DESCRIPTION_VAR, default=None)
            transaction_type = request.POST.get(TRANSACTION_TYPE_VAR, default='EXPENSE')

            try:
                new_transaction = Transaction.transaction_manager.create_transaction(
                    user=request.user,
                    category=Category.category_manager.retrieve_category(user=request.user).filter(name=category_name)[0],
                    amount=amount,
                    date=date,
                    description=description,
                    type=transaction_type,
                )

                return JsonResponse(model_to_dict(new_transaction))
            except:
                return JsonResponse({'message': 'Failed to create new transaction. Check Fields'})
            



            



            


