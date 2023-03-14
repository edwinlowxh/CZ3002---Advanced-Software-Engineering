import csv
import os
import traceback
from django.shortcuts import render, redirect

from .forms import *
from .models import *
from Finance.models import *
from Finance.FinanceMgr import *

from Budget.models import *
from Transaction.models import *

from .constants import (
    HDB_DOWN_PAYMENT_RATE,
    LOAN_PERIOD,
)

import json

from .pricing_helper import (
    calculate_down_payment,
    calculate_max_home_loan,
    calculate_monthly_installment,
    calculate_option_fee,
    calculate_stamp_duty,
    calculate_max_LTV
)

from django.utils.timezone import now
from django.contrib import messages

def form_view(request):
    if request.user.is_authenticated:
        user = request.user
        financeMgr = FinanceMgr(user)
        context = {}

        try:
            user.information
            if(user.information.debt_set.all().filter(debtName="House").exists()):
                context["estimatedMonthlySavings"] = financeMgr.calculateCashFlow(
                ) + user.information.debt_set.all().filter(debtName="House")[0].repayment
            else:
                context["estimatedMonthlySavings"] = financeMgr.calculateCashFlow()

        except:
            context["estimatedMonthlySavings"] = -1

        if request.method == "POST":
            if(request.POST):

                selected_locations = request.POST.getlist("towns[]")
                estimated_monthly_savings = request.POST.get(
                    "estimatedMonthlySavings")
                selected_property_types = request.POST.getlist("propertyType[]")


                # assuming housing loan instead of bank loan
                # 85% of maxPropertyPrice can be loaned, 15% downpayment over a loan period of 25 years
                monthly_installment = float(estimated_monthly_savings)
                max_home_loan = calculate_max_home_loan(monthly_installment)
                max_property_price = (1 / (1 - HDB_DOWN_PAYMENT_RATE)) * max_home_loan
                down_payment = HDB_DOWN_PAYMENT_RATE * max_property_price
                option_fee = calculate_option_fee(selected_property_types)
                stamp_duty = calculate_stamp_duty(max_property_price)
                lump_sum_payment = down_payment + option_fee + stamp_duty

                request.session['user_housing_financials'] = json.dumps(
                    {
                        'max_property_price': max_property_price,
                        'down_payment': down_payment,
                        'lump_sum_payment': lump_sum_payment,
                        'max_home_loan': max_home_loan,
                        'monthly_installment': monthly_installment,
                        'loan_period': LOAN_PERIOD
                    }
                )

                request.session['user_housing_preferences'] = json.dumps(
                    {
                        'preferred_property_type' : selected_property_types,
                        'estimated_monthly_savings' : estimated_monthly_savings,
                        'preferred_property_location' : selected_locations
                    }
                )

                return redirect('/house/costBreakdown/')

        elif request.method == 'GET':
            return render(request, 'house/form.html', context)
    else:
        return redirect('home')


def costBreakdown_view(request):
    if request.user.is_authenticated:

        username = request.user.username
        user_housing_financials = json.loads(request.session['user_housing_financials'])

        # Query database
        user = request.user
        try:
            # will give error if housinguserdata does not exist yet
            #financeMgr = FinanceMgr(user)
            if request.method == "POST":
              if(request.POST):                
                house_category = Category.category_manager.get_categories(user = user, name = "House Mortage")

                if not house_category:
                     category = Category.category_manager.create_category(user=user, name = "House Mortage")
                else:
                     category = house_category[0]

                #create Transaction
                house_transaction = Transaction.transaction_manager.create_transaction(user = user, 
                                                                                     amount = request.POST.get("repayment"), 
                                                                                     description= "Monthly Rent For House",
                                                                                     type = "EXPENSE",
                                                                                     category= category,
                                                                                     date = now().today())
                
                messages.success(request, "House Mortage sucessfully copied!" )
                return redirect("/transactions/")

            else:
                user_housing_preferences = json.loads(request.session['user_housing_preferences'])
                # User prefered location and type
                prefered_property_types = user_housing_preferences['preferred_property_type']
                prefered_locations = user_housing_preferences['preferred_property_location']


                # Get list of resale properties for all permutations of type and location
                resale_flat_list = []
                # workpath = os.path.dirname(os.path.abspath(__file__))
                # with open(os.path.join(workpath, 'resale-flat-prices-2021.csv'), 'r') as csv_file:
                #     reader = csv.reader(csv_file)
                #     for row in reader:
                #         if (row[1] in preferredLocation and row[2] in preferredPropertyType and float(row[3]) <= housingCalculate['maxPropertyPrice']):
                #             resaleList.append([row[1], row[2], float(row[3])])

                for i in prefered_property_types:
                    for j in prefered_locations:
                        resale_flat_list += ResaleFlatPrice.resale_flat_price_manager.retrieve_prices(
                            j, i, user_housing_financials['max_property_price'])

                # Sort the list of resale properties by price
                resale_flat_list = sorted(resale_flat_list, key=lambda x: x[2])
                if len(resale_flat_list) == 0:
                    messages.error(request, "No properties that meet your preferred location or prices found. Please try again!" )
                    redirect("/house/form/")
                most_affordable = resale_flat_list[0]
                max_affordable = resale_flat_list[-1]
                suggested_properties = []
                for location, property_type, property_price in [most_affordable, max_affordable]:                
                    max_LTV = calculate_max_LTV(property_price)
                    monthly_installment = calculate_monthly_installment(max_LTV=max_LTV, period=LOAN_PERIOD)
                    down_payment = calculate_down_payment(property_price)
                    option_fee = calculate_option_fee([property_type])
                    stamp_duty = calculate_stamp_duty(property_price)
                    lump_sum_payment = down_payment + option_fee + stamp_duty

                    suggested_properties.append({
                        'location' : location,
                        'type' : property_type,
                        'price' : property_price,
                        "maxLTV" : max_LTV,
                        'period' : 25,
                        'monthlyInstallment' : round(monthly_installment, 1),
                        'downPayment' : down_payment,
                        'buyerStampDuties' : stamp_duty,
                        'lumpSumPayment' : lump_sum_payment
                    })

                    # Round values
                    for key, value in user_housing_financials.items():
                        if (key != 'loanPeriod'):
                            user_housing_financials[key] = round(value, 1)

                return render(request, "house/costBreakdown.html", {'mostAffordable': suggested_properties[0], 'maxAffordable': suggested_properties[1], 'housingCalculate': user_housing_financials})
                # return render(request, "house/costBreakdown.html", {'mostAffordable': 1, 'maxAffordable': 1, 'housingCalculate': 1, 'username': 1, "firstTime": 1})
        except Exception as e:
            print(traceback.format_exc())
            return redirect("/house/form/")
    else:
        return redirect('home')
