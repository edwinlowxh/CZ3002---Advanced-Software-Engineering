from time import sleep
import traceback
from django.forms import model_to_dict
from django.shortcuts import redirect, render

from .models import Transaction

from .form.CreateTransactionForm import CreateTransactionForm

from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt

from FinApp.decorators import basic_auth

import json 

from django.core import serializers

from django.shortcuts import render, redirect
import pandas as pd
import os
from django.core.files.storage import FileSystemStorage
from Transaction.models import Transaction
from .form.UploadTransactionForm import UploadTransactionForm

from FinApp.settings import BASE_DIR
from django.contrib import messages
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

from django.contrib import messages

# Create your views here.

def transaction_view(request):
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
            # print(request.user, context)
            return render(request, 'transaction.html', context)
        
        if request.method == 'POST':
            if request.method == 'POST':
                if 'myfile' in request.FILES:     
                    fs = FileSystemStorage() 
                    user = request.user
                    myfile = request.FILES['myfile']
                    filename = fs.save(myfile.name, myfile)
                    file_path = os.path.join(BASE_DIR, fs.url(filename)[1:])
                    data = pd.read_csv(file_path, header = 0)    
                    data_dict = data.to_dict(orient='records')
                    
                    for row in data_dict:
                        form = UploadTransactionForm(request.user, **row)
                        if form.is_valid():
                            new_transaction = Transaction.transaction_manager.create_transaction(
                                user=request.user,
                                **form.cleaned_data
                            )
                        else:
                            messages.error(request, form.errors)
                            return redirect("/transactions/")
                    
                    messages.success(request, "Upload Successful!" )
                    return redirect("/transactions/")
            
    else:
        return redirect('/login')


@csrf_exempt
@basic_auth
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
            # print(request.user, context)
            return JsonResponse(context, status=201)
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
            return JsonResponse(context, status=201)
    else:
        return redirect('login')

@csrf_exempt
@basic_auth
def delete_transaction(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            id = request.POST.get(TRANSACTION_ID_VAR)

            try:
                Transaction.transaction_manager.delete_transaction(user=request.user, id=id)
                return JsonResponse({},status=201)
            except Exception as e:                
                return JsonResponse({'non_field_errors': 'Failed to delete transaction'}, status=422)
    else:
        return redirect('login')

@csrf_exempt
@basic_auth
def update_transaction(request, id: str=None):
    if request.user.is_authenticated:
        if request.method == 'POST':
            transaction_id = request.POST.get(TRANSACTION_ID_VAR)

            try:
                form_data = CreateTransactionForm.map_fields(request.POST.dict())
                form = CreateTransactionForm(request.user, **form_data)

                if form.is_valid():
                    updated_transaction = Transaction.transaction_manager.update_transaction(
                        user=request.user,
                        id=transaction_id,
                        **form.cleaned_data
                    )

                    if not updated_transaction:
                        return JsonResponse({'non_field_errors': 'Invalid Transaction'}, status=422)
                    else:
                        return JsonResponse(model_to_dict(updated_transaction), status=201)
                else:
                    return JsonResponse({'field_errors': CreateTransactionForm.map_fields(form.errors, reverse=True)}, status=422)

            except Exception as e:
                print(traceback.format_exc())           
                return JsonResponse({'non_field_errors': 'Failed to update transaction. Contact Administrator'}, status=500)
            
        elif request.method == 'GET':
            transaction_id = request.GET.get(TRANSACTION_ID_VAR)
            query_set = Transaction.transaction_manager.retrieve_transaction(user=request.user, id=transaction_id)
            serialized_data = json.loads(serializers.serialize('json', query_set, use_natural_foreign_keys=True, use_natural_primary_keys=True))

            for data in serialized_data:
                transaction = data["fields"]
                del transaction["user"]
                transaction.update({"id": data["pk"]})

            categories = Category.category_manager.get_categories(user=request.user)

            context = {
                'transaction': CreateTransactionForm.map_fields(serialized_data[0]['fields'], reverse=True),
                'categories': [model_to_dict(category)['name'] for category in categories]
            }

            return JsonResponse(context, status=200)
            return render(request, "", context)
    else:
        return redirect('login')


def Import_Excel(request):
    if request.method == 'POST':
        if 'myfile' in request.FILES:     
            fs = FileSystemStorage() 
            user = request.user
            myfile = request.FILES['myfile']
            filename = fs.save(myfile.name, myfile)
            file_path = os.path.join(BASE_DIR, fs.url(filename)[1:])
            data = pd.read_csv(file_path, header = 0)    
            data_dict = data.to_dict(orient='records')
            
            for row in data_dict:
              form = UploadTransactionForm(request.user, **row)
              if form.is_valid():
                new_transaction = Transaction.transaction_manager.create_transaction(
                    user=request.user,
                    **form.cleaned_data
                )
              else:
                messages.error(request, form.errors)
                return render(request, 'import_excel_db.html', {}) 
            
            messages.success(request, "Upload Successful!" )
            return redirect("transactions/")
            #return render(request, 'import_excel_db.html', {}) 
            #return redirect("transactions/")
           
    return render(request, 'import_excel_db.html',{})




            



            



            


