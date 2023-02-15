from django.contrib import admin
from .models import *

# Register your models here.
# class TransactionAdmin(admin.ModelAdmin):
#     list_display = ('user', 'amount', 'catergory', 'date', 'description', 'type')
admin.site.register(Transaction)

