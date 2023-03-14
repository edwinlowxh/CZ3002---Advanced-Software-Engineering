from __future__ import annotations

from django.db import models

from django.apps import apps

from django.contrib.auth.models import User

from typing import TYPE_CHECKING, Tuple

if TYPE_CHECKING:
    from Car.models import Trip

class UserTripManager(models.Manager):
    def get_trips(self, user: User) -> models.QuerySet:
        return super().get_queryset().get_or_create(
            user=user,
            defaults={
                'mileage': 0
            }
        )
    
    def update_trip(self, user: User, trip_id: int, source: str, destination: str, frequency: int, distance: float) -> Tuple[Trip, float]:
        Trip = apps.get_model('Car', 'Trip')
        old_trip = Trip.trip_manager.get_trip(id=trip_id)[0]

        if not old_trip:
            return None, 0
        
        old_distance = old_trip.distance
        old_frequency = old_trip.frequency

        trip = Trip.trip_manager.update_trip(id=trip_id, source=source, destination=destination, frequency=frequency, distance=distance)

        if not trip:
            return None, 0
        
        distance_difference = float(distance) * float(frequency) - float(old_distance) * float(old_frequency)
        user_trips = super().get_queryset().filter(user=user)[0]
        user_trips.mileage += distance_difference
        user_trips.save()

        return trip, user_trips.mileage

    def add_trip(self, user: User, source: str, destination: str, frequency: int, distance: float) -> Tuple[Trip, float]:
        Trip = apps.get_model('Car', 'Trip')
        new_trip = Trip.trip_manager.add_trip(source=source, destination=destination, frequency=frequency, distance=distance)

        if not new_trip:
            return None, 0

        user_trips = self.get_trips(user=user)[0]
        user_trips.trips.add(new_trip)
        user_trips.mileage += float(new_trip.distance) * float(new_trip.frequency)
        user_trips.save()

        return new_trip, user_trips.mileage

    def delete_trip(self, user: User, trip_id: int) -> float:
        Trip = apps.get_model('Car', 'Trip')
        trip = Trip.trip_manager.get_trip(trip_id)

        if trip:
            trip = trip[0]
            user_trips = self.get_trips(user=user)[0]
            user_trips.trips.remove(trip)
            user_trips.mileage -= float(trip.distance) * float(trip.frequency)
            user_trips.save()

        return user_trips.mileage