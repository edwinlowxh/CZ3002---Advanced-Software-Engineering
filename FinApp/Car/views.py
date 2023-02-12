from django.shortcuts import render, redirect, reverse
from django.db.models import Q
from .models import (
    Car,
    Trip,
    UserTrip
)
from .carMgr import *
from .tripMgr import *
from Finance.models import Information
from Finance.FinanceMgr import *

from Car.helper.CarHelper import(
    calc_cost
)

def search_view(request):
    if request.session.has_key('username'):
        username = request.session['username']

        if Information.objects.filter(user = username).exists():
            firstTime = False
        else:
            firstTime = True

        return render(request, 'car/search.html', {"username" : username, "firstTime": firstTime})
    else:
        return render(request, 'car/search.html', {})


def results_view(request):
    if request.session.has_key('username'):
        username = request.session['username']

        query = request.GET.get('search')
        car_list = Car.car_manager.search(query)
        car_list.order_by('model')

        if not car_list:
            errors = True
        else:
            errors = False

        return render(request, "car/results.html", {"car_list" : car_list, "username" : username, "errors" : errors})
    else:
        return render(request, 'car/results.html', {})


def details_view(request, pk):
    if request.session.has_key('username'):
        username = request.session['username']

        car = Car.car_manager.get_car(pk)[0]  
        tripMgr = TripMgr()
        user = User.user.get(username=username)
        user_trips = UserTrip.user_trip_manager.get_trips(user=user)[0]
        trips = user_trips.trips.all()
        mileage = user_trips.mileage
        totalCost = calc_cost(car, mileage)

        if request.method == 'POST':  # Add trip
            if 'Add trip' in request.POST:
                source = request.POST.get('source')
                destination = request.POST.get('destination')
                frequency = request.POST.get('frequency')
                tripMgr.addTrip(source, destination, frequency)
                tripMgr.addTripDB()
                tripMgr.addUserTripDB(user)
                return redirect(reverse('car_details', kwargs={'pk': pk}))
            elif 'Update Balance Sheet' in request.POST:
                financeMgr = FinanceMgr(user)

                if(user.information.debt_set.all().filter(debtName="Car").exists()):
                    financeMgr.updateDebt(user.information.debt_set.all().filter(debtName="Car")[0].id,
                                          "Car",  car.currentPrice, totalCost, 0.0)
                else:
                    financeMgr.createDebt("Car", car.currentPrice,
                                          totalCost, 0.0)

                if(user.information.asset_set.all().filter(assetName="Car").exists()):
                    financeMgr.updateAsset(user.information.asset_set.all().filter(assetName="Car")[0].id,
                                           "Car", car.currentPrice, -0.10)
                else:
                    financeMgr.createAsset(
                        "Car", car.currentPrice, -0.10)
                #Redirect
                return redirect("/../finance/balanceSheet_Result/")

        context={
            'car':car,
            'trips':trips,
            'totalMileage':mileage / 1000,
            'username':username,
            'totalCost': round(totalCost, 2),
        }

        return render(request, "car/details.html", context)
    else:
        return render(request, 'car/details.html', {})


def trip_delete(request, pk):

    if request.session.has_key('username'):
        username = request.session['username']

        if Information.objects.filter(user = username).exists():
            firstTime = False
        else:
            firstTime = True

        if request.method == 'POST':
            return redirect(reverse('car_details', kwargs={'pk': pk}))
        tripMgr = TripMgr()
        user = User.user.get(username=username)
        trips = tripMgr.getUserTripDB(user)

        tripMgr.deleteTrip(-1)
        tripMgr.addUserTripDB(user)

        return render(request, 'car/trip_delete.html', {"username" : username, "firstTime": firstTime})
    else:
        return render(request, 'car/trip_delete.html', {})
