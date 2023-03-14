from __future__ import annotations
import os

from django.db import models

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Car.models import Trip

import requests

class TripManager(models.Manager):
    def get_trip(self, id: int):
        return super().get_queryset().filter(id=id)

    def add_trip(self, source: str, destination: str, frequency: int, distance: float) -> Trip:
        trip = self.create(source=source, destination=destination, frequency=frequency, distance=distance)
        return trip

    def delete_trip(self, id: int) -> None:
        trip = self.filter(id=id)
        trip.delete()

    def update_trip(self, id: int, source: str, destination: str, frequency: int, distance: float) -> Trip:
        query_set = super().get_queryset().filter(id=id)
        
        if not query_set:
            return None
        else:
            query_set.update(
                source=source,
                destination=destination,
                frequency=frequency,
                distance=distance,
            )

        return query_set[0]

    @staticmethod
    def calculate_distance(source, destination):
        source += " Singapore"
        destination += " Singapore"

        #Base url
        url = "https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&"
        
        # Get api key
        f = open('./Car/manager/api_key.txt', 'r')
        api_key = f.read()
        f.close()

        #get response
        r = requests.get(url + "origins=" + source + "&destinations=" + destination + "&key=" + api_key)
        distance = r.json()['rows'][0]['elements'][0]['distance']['value']
        return distance
    