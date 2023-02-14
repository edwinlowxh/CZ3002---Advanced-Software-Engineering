from typing import List

from django.db import models

from Main.models import User

class HousingDataManager(models.Manager):

    def retrieve_housing_data(self,user):
        housingUserData = super().get_queryset().filter(user=user)
        housingUserData = housingUserData[0]
        return {
            "user":housingUserData.user,
            "preferred_property_type": housingUserData.preferred_property_type,
            "estimated_monthly_savings": housingUserData.estimated_monthly_savings,
            "preferred_property_location": housingUserData.preferred_property_location
        }

    def create_housing_data(self,user,preferredPropertyType,estimatedMonthlySavings,preferredLocation):
        return super().create(user=user,
               preferredPropertyType=preferredPropertyType,
               estimatedMonthlySavings=estimatedMonthlySavings,
               preferredLocation=preferredLocation)

    def update_housing_data(self,user: User, preferred_property_type: str, estimated_monthly_savings: float,  preferred_property_location: str) -> None:
        query_set = self.get_queryset().filter(user=user)
        query_set.update_or_create(
            user = User,
            defaults = {
                'preferred_property_type': preferred_property_type,
                'estimated_monthly_savings': estimated_monthly_savings,
                'preferred_property_location': preferred_property_location
            }
        )

class ResaleFlatPriceManager(models.Manager):
    def retrieve_prices(self, prefered_location: List[str], preferred_property_type: List[str], max_price: float) -> list:
        query = self.get_queryset().filter(location = prefered_location, flatType = preferred_property_type, propertyPrice__lte = max_price)
        resaleFlatPriceList = []
        for i in query:
            resaleFlatPriceList.append([i.location, i.flatType, i.propertyPrice])
        return resaleFlatPriceList