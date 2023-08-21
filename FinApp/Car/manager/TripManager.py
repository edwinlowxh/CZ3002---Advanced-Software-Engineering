from __future__ import annotations
import os

from django.db import models

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Car.models import Trip

import requests
import googlemaps

class TripManager(models.Manager):
    def get_trip(self, id: int):
        return super().get_queryset().filter(id=id)

    def add_trip(self, source: str, destination: str, 
                 frequency: int, distance: float, 
                 source_lat: str, source_long: str,
                 destination_lat: str, destination_long: str) -> Trip:
        trip = self.create(source=source, destination=destination, 
                           frequency=frequency, distance=distance,
                           source_lat=source_lat, source_long=source_long,
                           destination_lat=destination_lat, destination_long=destination_long)
        return trip

    def delete_trip(self, id: int) -> None:
        trip = self.filter(id=id)
        trip.delete()

    def update_trip(self, id: int, source: str, destination: str, frequency: int, distance: float,
                    source_lat: str, source_long: str,
                    destination_lat: str, destination_long: str) -> Trip:
        query_set = super().get_queryset().filter(id=id)
        
        if not query_set:
            return None
        else:
            query_set.update(
                source=source, destination=destination, frequency=frequency, distance=distance,
                source_lat=source_lat, source_long=source_long,
                destination_lat=destination_lat, destination_long=destination_long
            )

        return query_set[0]

    @staticmethod
    def calculate_distance(source, destination):
        #Base url
        url = "https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&"
        api_key = ""
        gmaps = googlemaps.Client(key=api_key)
        result = gmaps.distance_matrix(origins=source, destinations=destination, mode='driving')
        print(result)
        distance = result['rows'][0]['elements'][0]['distance']['value']
        return distance
    