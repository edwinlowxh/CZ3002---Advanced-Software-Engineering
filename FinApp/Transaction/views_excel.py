from django.shortcuts import render, redirect
import pandas as pd
import os
from django.core.files.storage import FileSystemStorage
from Transaction.models import Transaction
from .form.UploadTransactionForm import UploadTransactionForm

from FinApp.settings import BASE_DIR
from django.contrib import messages

 
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
                return render(request, 'Import_excel_db.html', {}) 
            
            messages.success(request, "Upload Successful!" )
            return redirect("transactions/")
            
    return render(request, 'Import_excel_db.html',{})

