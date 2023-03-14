"""FinApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

from Main.views import (
    registration_view,
    logout_view,
    login_view,
    account_view,
    home_view,
    password_change_view,
    verify_username_view,
    password_reset_view,
    password_reset_confirm_view,
    password_reset_complete_view,
)

from Car.views import (
    delete_trip,
    get_trip,
    search_view,
    results_view,
    details_view,
    update_trip,
)

from Finance.views import (
    financeHome_view,
    questionaire_view,
    balanceSheet_Result_view,
    balanceSheet_Edit_view,
    cashFlow_Result_view,
    cashFlow_Edit_view,
    growWealth_view,
    formError_view,
    updateError_view,
    updateUserInfo_View,
)

from House.views import (
    form_view,
    costBreakdown_view,
)

from user_profile.views import (
    register,
    login,
    logout,
    change_password,
    forget_password,
    update_user_information
)

from Transaction.views import(
    get_transactions,
    create_transaction,
    delete_transaction,
    transaction_view,
    update_transaction,
)

from Budget.views_category import(
    create_category,
    delete_category,
    update_category,
    get_category
)

from Budget.views_budget import(
    budget_view,
    get_budget,
    create_budget,
    delete_budget,
    update_budget
)

from Budget.views_home import (
    get_budget_home,
  )

from Transaction.views_stats import (
     get_filter_options,
     get_category_spending,
     get_income_expense_year,
     get_expense_monthly,
     statistics_view,)

{
  

}
urlpatterns = [
    path('admin/', admin.site.urls),
    # path('register/', registration_view, name="register"),
    # path('logout/', logout_view, name="logout"),
    # path('login/', login_view, name="login"),
    # path('account/', account_view, name="account"),
    # path('password_change/', password_change_view, name='password_change'),
    #path('', home_view, name="home"), 
    path('', get_budget_home, name='home'),

    # Car urls
    path('car/search/', search_view, name="car_search"),
    path('car/results/', results_view, name="car_results"),
    path('car/details/<int:pk>/', details_view, name="car_details"),
    path('car/delete_trip/', delete_trip, name="trip_delete"),
    path('car/get_trip/', get_trip, name="get_trip"),
    path('car/update_trip/', update_trip, name="update_trip"),

    # Password reset Urls
    path('password_reset_confirm/<username>/', password_reset_confirm_view, name='password_reset_confirm'),
    path('password_reset/', password_reset_view, name='password_reset'),
    path('verify_username/', verify_username_view, name='verify_username'),
    path('password_reset_complete/', password_reset_complete_view ,name='password_reset_complete'),

    # Path for house pages
    path('house/form/', form_view, name = 'form'),
    path('house/costBreakdown/', costBreakdown_view, name = 'costBreakdown'),

    # Path for user profile
    path('register/', register, name="register"),
    path('login/', login, name="login"),
    path('logout/', logout, name="logout"),
    path('profile/change_password/', change_password, name="change_password"),
    # path('profile/forget_password/', forget_password, name="forget_password"),
    path('profile/update_information/', update_user_information, name="update_user_information"),

    # Path for transactions
    path('transactions/', transaction_view, name = 'transactions'),
    path('transactions/get', get_transactions, name = 'get_transactions'),
    path('transactions/create', create_transaction, name = 'create_transactions'),
    path('transactions/delete', delete_transaction, name = 'delete_transactions'),
    path('transactions/update', update_transaction, name = 'update_transactions'),
    

    # Path for category
    path('categories/', get_category, name='get_category'),
    path('budget/create_category', create_category, name='create_category'),
    path('budget/delete_category', delete_category, name='delete_category'),
    path('budget/update_category', update_category, name='update_category'),

    # Path for budget
    path('budgets/', budget_view, name='budget'),
    path("budgets/get", get_budget, name="get_budget"),
    # path('budget/create_budget', create_budget, name='create_budget'),
    # path('budget/delete_budget', delete_budget, name='delete_budget'),
    path('budgets/update_budget', update_budget, name='update_budget'),
   
    path('pie/<int:year>/<int:month>', get_category_spending, name='get_category_spending'),
    path('stats',  statistics_view, name='stats'),
    path('chart/filter-options/', get_filter_options, name='chart-filter-options'),
    path('line/<int:year>/', get_income_expense_year, name='get_income_expense_year'),
    path('monthly_expense/<int:year>/<int:month>', get_expense_monthly, name='get_expense_monthly'),
    

    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# Old urls
# Path for finance pages
# path('finance/questionaire/', questionaire_view, name="questionaire"),
# path('finance/balanceSheet_Result/', balanceSheet_Result_view, name="balanceSheet_Result"),
# path('finance/balanceSheet_Edit/', balanceSheet_Edit_view, name="balanceSheet_Edit"),
# path('finance/cashFlow_Result/', cashFlow_Result_view, name="cashFlow_Result"),
# path('finance/cashFlow_Edit/', cashFlow_Edit_view, name="cashFlow_Edit"),
# path('finance/financeHome/', financeHome_view, name="financeHome"),
# path('finance/formError/', formError_view, name="formError"),
# path('finance/growWealth/', growWealth_view, name="growWealth"),
# path('finance/updateUserInfo/', updateUserInfo_View, name="updateUserInfo"),
# path('finance/updateError/', updateError_view, name="updateError"),