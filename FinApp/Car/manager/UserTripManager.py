from django.db import models

from django.apps import apps

from Main.models import User

class UserTripManager(models.Manager):
    def get_trips(self, user: User) -> models.QuerySet:
        return super().get_queryset().get_or_create(
            user=user,
            defaults={
                'mileage': 0
            }
        )

    def add_trip(self, user: User, source: str, destination: str, frequency: int, distance: float) -> None:
        Trip = apps.get_model('FinApp', 'Trip')
        new_trip = Trip.trip_manager.add_trip(source=source, destination=destination, frequency=frequency, distance=distance)

        user_trips = self.get_trips(user=user)[0]
        user_trips.trip.add(new_trip)
        user_trips.mileage += new_trip.distance
        user_trips.save()

    def delete_trip(self, user: User, trip_id: int) -> None:
        Trip = apps.get_model('FinApp', 'Trip')
        trip = Trip.trip_manager.get_trip(trip_id)

        if trip:
            trip = trip[0]
            user_trips = self.get_trips(user=user)[0]
            user_trips.trip.remove(trip)
            user_trips.mileage -= trip.distance
            user_trips.save()