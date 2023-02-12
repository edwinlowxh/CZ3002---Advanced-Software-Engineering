from django.contrib import admin
from .models import *

# Register your models here.
class CarAdmin(admin.ModelAdmin):
    list_display = ('make', 'model', 'spec', 'current_price', 'depreciation', 'down_payment',
                    'installment', 'COE', 'road_tax', 'OMV', 'ARF', 'fuel_economy', 'fuel_type', 'COE_Incl', 'image')

class FuelAdmin(admin.ModelAdmin):
    list_display = ('fuel_type', 'fuel_price')

class TripAdmin(admin.ModelAdmin):
    list_display = ('source', 'destination', 'frequency', 'distance')

class UserTripAdmin(admin.ModelAdmin):
    list_display = ('user', 'mileage')

admin.site.register(Car, CarAdmin)
admin.site.register(Fuel, FuelAdmin)
admin.site.register(Trip, TripAdmin)
admin.site.register(UserTrip, UserTripAdmin)
