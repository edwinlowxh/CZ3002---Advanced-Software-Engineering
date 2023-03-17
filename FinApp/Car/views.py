from django.forms import model_to_dict

from django.http import JsonResponse

from django.shortcuts import render, redirect, reverse

from django.views.decorators.csrf import csrf_exempt

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
    DESTINATION_VAR,
    FREQUENCY_VAR,
    SOURCE_VAR,
    TRIP_ID_VAR,
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
        if request.method == 'POST':  # Add trip
            if 'create_trip' in request.POST:
                source = request.POST.get('source')
                destination = request.POST.get('destination')
                frequency = request.POST.get('frequency')
                source_lat = float(request.POST.get('source_lat'))
                source_long = float(request.POST.get('source_long'))
                destination_lat = float(request.POST.get('destination_lat'))
                destination_long = float(request.POST.get('destination_long'))
            
                distance = Trip.trip_manager.calculate_distance(source=f'{source_lat},{source_long}',
                                                                destination=f'{destination_lat},{destination_long}')

                if distance == 0:
                    return JsonResponse({'message': 'Failed to add trip', 'non_field_errors': 'Unable to calculate trip distance for specified source and destination. Contact Administrator'}, status=500)
                
                trip, mileage = UserTrip.user_trip_manager.add_trip(
                    user=request.user, source=source, destination=destination, frequency=frequency, distance=distance,
                    source_lat=source_lat, source_long=source_long,
                    destination_lat=destination_lat, destination_long=destination_long    
                )
                
                return JsonResponse(model_to_dict(trip), status=201)
            
            elif 'update_balance_sheet' in request.POST:
                # Create category
                car_category = Category.category_manager.get_categories(user=request.user, name = "Car Mortgage")

                if not car_category:
                     category = Category.category_manager.create_category(user=request.user, name = "Car Mortgage")
                else:
                     category = car_category[0]
                
                car = Car.car_manager.get_car(pk)[0]  
                total_cost = calc_cost(car, mileage)

                car_transaction = Transaction.transaction_manager.create_transaction(
                    user = request.user, 
                    amount = round(total_cost,2), 
                    description= "rent for " + car.model + car.spec,
                    type = "EXPENSE",
                    category= category,
                    date = now().today()
                )

                messages.success(request, "Car Expense sucessfully copied!" )
                return redirect("/transactions/")
        elif request.method =='GET':
            car = Car.car_manager.get_car(pk)[0]  
            user_trips = UserTrip.user_trip_manager.get_trips(user=request.user)[0]
            trips = user_trips.trips.all()
            mileage = user_trips.mileage
            total_cost = calc_cost(car, mileage)
            context={
                'car':model_to_dict(car),
                'trips':trips,
                'total_mileage':mileage / 1000,
                'total_cost': round(total_cost, 2),
                'car_table_header': CAR_TABLE_HEADER,
                'trip_table_header': TRIP_TABLE_HEADER
            }

            return render(request, "car/details.html", context)
    else:
        return redirect('login')

@csrf_exempt    
def delete_trip(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            trip_id = request.POST.get(TRIP_ID_VAR)
            
            if not trip_id:
                return JsonResponse({'message': 'Failed to delete trip', 'non_field_errors': 'Please provide a trip id'}, status=422)

            try:
                mileage = UserTrip.user_trip_manager.delete_trip(user=request.user, trip_id=trip_id)
                return JsonResponse({}, status=201)
            except Exception as e:                
                return JsonResponse({'message': 'Failed to delete trip', 'non_field_errors': 'Failed to delete trip. Contact Administrator'}, status=500)

@csrf_exempt    
def get_trip(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            trip_id = request.POST.get(TRIP_ID_VAR)
            trip = Trip.trip_manager.get_trip(id=trip_id)[0]

            if not trip:
                return JsonResponse({'message': 'Failed to retrieve trip details', 'non_field_errors': 'Failed to retrieve trip. Contact Administrator'}, status=500)
            
            user_trips = UserTrip.user_trip_manager.get_trips(user=request.user)[0]
            trips = user_trips.trips.all()

            if trip not in trips:
                return JsonResponse({'message': 'Failed to retrieve trip details', 'non_field_errors': 'Failed to retrieve trip details. Contact Administrator'}, status=500)
            else:
                print(model_to_dict(trip))
                return JsonResponse({'trip': model_to_dict(trip)}, status=200)
            
@csrf_exempt    
def update_trip(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            trip_id = request.POST.get(TRIP_ID_VAR)
            trip = Trip.trip_manager.get_trip(id=trip_id)[0]

            if not trip:
                return JsonResponse({'message': 'Failed to retrieve trip details', 'non_field_errors': 'Failed to retrieve trip details. Contact Administrator'}, status=500)
            
            user_trips = UserTrip.user_trip_manager.get_trips(user=request.user)[0]
            trips = user_trips.trips.all()

            if trip not in trips:
                return JsonResponse({'message': 'Failed to retrieve trip details', 'non_field_errors': 'Failed to retrieve trip details. Contact Administrator'}, status=500)
            else:
                source = request.POST.get(SOURCE_VAR)
                destination = request.POST.get(DESTINATION_VAR)
                frequency = request.POST.get(FREQUENCY_VAR)
                source_lat = float(request.POST.get('source_lat'))
                source_long = float(request.POST.get('source_long'))
                destination_lat = float(request.POST.get('destination_lat'))
                destination_long = float(request.POST.get('destination_long'))
            
                distance = Trip.trip_manager.calculate_distance(source=f'{source_lat},{source_long}',
                                                                destination=f'{destination_lat},{destination_long}')

                if distance == 0:
                    return JsonResponse({'message': 'Failed to update trip', 'non_field_errors': 'Unable to calculate trip distance for specified source and destination'}, status=500)

                trip, mileage = UserTrip.user_trip_manager.update_trip(
                    trip_id=trip_id, user=request.user, source=source, destination=destination, frequency=frequency, distance=distance,
                    source_lat=source_lat, source_long=source_long,
                    destination_lat=destination_lat, destination_long=destination_long    
                )

                if not trip:
                    return JsonResponse({'message': 'Failed to update trip', 'non_field_errors': 'Unable to update trip. Contact Administrator'}, status=500)

                return JsonResponse(model_to_dict(trip), status=200)



@csrf_exempt          
def save_location(request):
    if request.method == 'POST':
        source_lat = request.POST.get('source_lat')
        source_lng = request.POST.get('source_lng')
        dest_lat = request.POST.get('dest_lat')
        dest_lng = request.POST.get('dest_lng')
        # do something with the location data
        print(source_lat)
        print(source_lng)
        print(dest_lng)
        print(dest_lat)
        print(
            Trip.trip_manager.calculate_distance(
                source=f'{source_lat},{source_lng}',
                destination=f'{dest_lat},{dest_lng}'
            )
        )
        # e.g. save it to a database
    return render(request, 'car/google_maps.html')