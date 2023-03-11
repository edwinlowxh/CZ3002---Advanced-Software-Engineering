from django.forms import model_to_dict
from django.shortcuts import render, redirect, reverse
from django.db.models import Q

from .models import (
    Car,
    Trip,
    UserTrip
)

from Finance.models import Information
from Finance.FinanceMgr import *

from Budget.models import *
from Transaction.models import *

from Car.helper.CarHelper import(
    calc_cost
)

from .constants import (
    CAR_TABLE_HEADER,
    TRIP_TABLE_HEADER
)

from django.utils.timezone import now
from django.contrib import messages

def search_view(request):
    if request.user.is_authenticated:
        return render(request, 'car/search.html')
    else:
        return render(request, 'car/search.html')


def results_view(request):
    if request.user.is_authenticated:

        query = request.GET.get('search')
        limit = request.GET.get('estimatedMonthlySavings')
        if limit == "":
             car_list = Car.car_manager.search(query, 1000000000)
        else: 
             car_list = Car.car_manager.search(query, float(limit))
        car_list = car_list.order_by('installment')

        if not car_list:
            errors = True
        else:
            errors = False

        return render(request, "car/results.html", {"car_list" : car_list, "errors" : errors})
    else:
        return render(request, 'car/results.html', {})


def details_view(request, pk):
    if request.user.is_authenticated:

        car = Car.car_manager.get_car(pk)[0]  
        # tripMgr = TripMgr()
        user = request.user
        user_trips = UserTrip.user_trip_manager.get_trips(user=user)[0]
        trips = user_trips.trips.all()
        mileage = user_trips.mileage
        totalCost = calc_cost(car, mileage)

        if request.method == 'POST':  # Add trip
            if 'Add trip' in request.POST:
                # source = request.POST.get('source')
                # destination = request.POST.get('destination')
                # frequency = request.POST.get('frequency')
                # tripMgr.addTrip(source, destination, frequency)
                # tripMgr.addTripDB()
                # tripMgr.addUserTripDB(user)

                # TODO: Take reference from code on top and implement with new TripManager.py
                return redirect(reverse('car_details', kwargs={'pk': pk}))
            # elif 'Update Balance Sheet' in request.POST:
            #     financeMgr = FinanceMgr(user)

            #     if(user.information.debt_set.all().filter(debtName="Car").exists()):
            #         financeMgr.updateDebt(user.information.debt_set.all().filter(debtName="Car")[0].id,
            #                               "Car",  car.currentPrice, totalCost, 0.0)
            #     else:
            #         financeMgr.createDebt("Car", car.currentPrice,
            #                               totalCost, 0.0)

            #     if(user.information.asset_set.all().filter(assetName="Car").exists()):
            #         financeMgr.updateAsset(user.information.asset_set.all().filter(assetName="Car")[0].id,
            #                                "Car", car.currentPrice, -0.10)
            #     else:
            #         financeMgr.createAsset(
            #             "Car", car.currentPrice, -0.10)
            #     #Redirect
            #     return redirect("/../finance/balanceSheet_Result/")
            
            elif 'Update Balance Sheet' in request.POST:
                # Create category
                car_category = Category.category_manager.get_categories(user = user, name = "Car Mortage")

                if not car_category:
                     category = Category.category_manager.create_category(user=user, name = "Car Mortage")
                else:
                     category = car_category[0]

                car_transaction = Transaction.transaction_manager.create_transaction(user = user, 
                                                                                     amount = round(totalCost,2), 
                                                                                     description= "rent for " + car.model + car.spec,
                                                                                     type = "EXPENSE",
                                                                                     category= category,
                                                                                     date = now().today())

                messages.success(request, "Car Expense sucessfully copied!" )
                return redirect("/transactions/")

                

        context={
            'car':model_to_dict(car),
            'trips':trips,
            'total_mileage':mileage / 1000,
            'total_cost': round(totalCost, 2),
            'car_table_header': CAR_TABLE_HEADER,
            'trip_table_header': TRIP_TABLE_HEADER
        }

        return render(request, "car/details.html", context)
    else:
        return render(request, 'car/details.html', {})


def trip_delete(request, pk):
    if request.user.is_authenticated:
        if request.method == 'POST':
            return redirect(reverse('car_details', kwargs={'pk': pk}))
        # tripMgr = TripMgr()
        # trips = tripMgr.getUserTripDB(request.user)

        # tripMgr.deleteTrip(-1)
        # tripMgr.addUserTripDB(request.user)
        # TODO: Take reference from code on top and implement with new TripManager.py

        return render(request, 'car/trip_delete.html')
    else:
        return render(request, 'car/trip_delete.html')
