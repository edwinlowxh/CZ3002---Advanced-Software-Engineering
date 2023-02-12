from __future__ import annotations

from django.db import models

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Car.models import Trip

class TripManager(models.Manager):
    def get_trip(self, id: int):
        return super().get_queryset().filter(id=id)

    def add_trip(self, source: str, destination: str, frequency: int, distance: float) -> Trip:
        trip = self.create(source=source, destination=destination, frequency=frequency, distance=distance)
        return trip

    def delete_trip(self, id: int) -> None:
        trip = self.filter(id=id)
        trip.delete()