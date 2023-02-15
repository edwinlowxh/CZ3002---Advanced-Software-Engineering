from django.contrib import admin
from .models import *

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'name')

class BudgetAdmin(admin.ModelAdmin):
    list_display = ('user', 'limit', 'date', 'category')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Budget, BudgetAdmin)
