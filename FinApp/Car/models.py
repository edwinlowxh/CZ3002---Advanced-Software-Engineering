from django.db import models
from django.contrib.auth.models import User

from Car.manager.CarManager import CarManager
from Car.manager.TripManager import TripManager
from Car.manager.UserTripManager import UserTripManager

# Create your models here.
class Car(models.Model):
    id = models.IntegerField(primary_key=True)
    make = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    spec = models.CharField(max_length=255)
    current_price = models.FloatField(null=True)
    depreciation = models.FloatField(null=True)
    down_payment = models.FloatField(null=True)
    installment = models.FloatField(null=True)
    COE = models.FloatField(null=True)
    road_tax = models.FloatField(null=True)
    OMV = models.FloatField(null=True)
    ARF = models.FloatField(null=True)
    fuel_economy = models.FloatField(null=True)
    fuel_type = models.CharField(max_length=255)
    COE_Incl = models.BooleanField(default=True)
    image = models.ImageField(upload_to='images/')
    car_manager = CarManager()

    class Meta:
        unique_together = ('make', 'model', 'spec')

class Fuel(models.Model):
    fuel_type = models.CharField(max_length=255, primary_key=True)
    fuel_price = models.FloatField()

class Trip(models.Model):
    id = models.AutoField(primary_key=True)
    source = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    source_lat = models.FloatField()
    source_long = models.FloatField()
    destination_lat = models.FloatField()
    destination_long = models.FloatField()
    frequency = models.IntegerField()
    distance = models.FloatField()
    trip_manager = TripManager()


class UserTrip(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    trips = models.ManyToManyField(Trip, blank=True)
    mileage = models.FloatField()
    user_trip_manager = UserTripManager()
