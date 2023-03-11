from django.http import JsonResponse
from .utils.charts import months, colorPrimary, colorSuccess, colorDanger, generate_color_palette, get_year_dict
from Transaction.models import Transaction
from Budget.models import Category
from django.http import JsonResponse
from django.shortcuts import render


def get_filter_options(request):
    options = [2020,2021,2022,2023]
    months = [x for x in range(1,13)]

    return JsonResponse({
        'options': options,
        'months' : months
    })


def get_category_spending(request, year, month):
    labels = []
    data = []
    
    user = request.user
    categories = Category.category_manager.get_categories(user = user, is_active = True)
    for category in categories:
        labels.append(category.name)
        data.append(Transaction.transaction_manager.retrieve_total_expenses(user=user, category = category,year=year,month=month,type="EXPENSE")["amount__sum"] or 0)
    
    return JsonResponse({
        'title': f'Spending by Category for {months[month-1]}, {year}',
        'data': {
            'labels': labels,
            'datasets': [{
                'label': 'Amount ($)',
                'backgroundColor': generate_color_palette(len(labels)),
                'borderColor': generate_color_palette(len(labels)),
                'data': data,
            }]
        },
    })
    
def get_income_expense_year(request, year):
    income = []
    expense = []

    user = request.user

    for x in range(1,13):
        expense.append(Transaction.transaction_manager.retrieve_total_expenses(user=user, year=year,month=x, type= "EXPENSE")["amount__sum"] or 0)
        income.append(Transaction.transaction_manager.retrieve_total_expenses(user=user, year=year,month=x, type = "INCOME")["amount__sum"] or 0)

    return JsonResponse({
        'title': f'Income and Expense for {year}',
        'data': {
            'labels': months,
            'datasets': [{
                'label': ["Expense"],
                #'backgroundColor': "#55efc4",
                'borderColor': colorPrimary,
                'data': expense,
            },
            {
                'label': "Income",
                #'backgroundColor': '#a29bfe',
                'borderColor': colorPrimary,
                'data': income,
            }]
        },
    })


def statistics_view(request):
    return render(request, 'statistics.html', {})

