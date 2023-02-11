import csv
import os
import traceback
from django.shortcuts import render, redirect

from .forms import *
from .models import *
from Finance.models import *
from Finance.FinanceMgr import *

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

def form_view(request):
    if request.session.has_key('username'):
        username = request.session['username']
        user = User.user.get(username=username)
        financeMgr = FinanceMgr(user)
        if Information.objects.filter(user=username).exists():
            firstTime = False
        else:
            firstTime = True

        context = {"username": username, "firstTime": firstTime}

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
                # user = User.user.validate("Main_user2","main12345")

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
    if request.session.has_key('username'):

        username = request.session['username']
        user_housing_financials = json.loads(request.session['user_housing_financials'])

        if Information.objects.filter(user=username).exists():
            firstTime = False
        else:
            firstTime = True

        # Query database
        user = User.user.get(username=username)
        try:
            # will give error if housinguserdata does not exist yet
            user.housinguserdata
            financeMgr = FinanceMgr(user)
            if(request.POST):
                try:
                    user.information
                    financeMgr = FinanceMgr(user)
                    if(user.information.debt_set.all().filter(debtName="House").exists()):
                        financeMgr.updateDebt(user.information.debt_set.all().filter(debtName="House")[0].id,
                                              "House",  request.POST.get("price"), request.POST.get("repayment"), 0.026)
                    else:
                        financeMgr.createDebt("House", request.POST.get("price"),
                                              request.POST.get("repayment"), 0.026)
                    if(user.information.asset_set.all().filter(assetName="House").exists()):
                        financeMgr.updateAsset(user.information.asset_set.all().filter(assetName="House")[0].id,
                                               "House", request.POST.get("price"), 0)
                    else:
                        financeMgr.createAsset(
                            "House", request.POST.get("price"), 0)
                    return redirect("/finance/balanceSheet_Result/")
                except:
                    return redirect("/finance/questionaire/")

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

                return render(request, "house/costBreakdown.html", {'mostAffordable': suggested_properties[0], 'maxAffordable': suggested_properties[1], 'housingCalculate': user_housing_financials, 'username': username, "firstTime": firstTime})
        except Exception as e:
            print(traceback.format_exc())
            return redirect("/house/form/")
    else:
        return redirect('home')
