from django.db import models
# from Main.models import *
from Finance.models import *
from Main.models import *
from multiselectfield import MultiSelectField

from House.manager import (
    HousingDataManager,
    ResaleFlatPriceManager
)

from House.constants import (
    LOCATIONS_LIST,
    PROPERTY_TYPES_LIST
)

# Create your models here.

# class HousingDataMgr(models.Manager):

#     def retrieveHousingData(self,user):
#         housingUserData = self.get_queryset().filter(user=user)
#         housingUserData = housingUserData[0]
#         return {
#             "user":housingUserData.user,
#             "preferredPropertyType": housingUserData.preferredPropertyType,
#             "estimatedMonthlySavings": housingUserData.estimatedMonthlySavings,
#             "preferredLocation": housingUserData.preferredLocation
#         }
#     def createHousingData(self,user,preferredPropertyType,estimatedMonthlySavings,preferredLocation):
#         return self.create(user=user,
#                preferredPropertyType=preferredPropertyType,
#                estimatedMonthlySavings=estimatedMonthlySavings,
#                preferredLocation=preferredLocation)

#     def updateHousingData(self,user,preferredPropertyType,estimatedMonthlySavings,preferredLocation):
#         housingUserData = self.get_queryset().filter(user=user)
#         housingUserData = housingUserData[0]
#         housingUserData.preferredPropertyType = preferredPropertyType
#         housingUserData.estimatedMonthlySavings = estimatedMonthlySavings
#         housingUserData.preferredLocation = preferredLocation
#         housingUserData.save()

class HousingUserData(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        to_field= "username",
        default = None,
        primary_key= True
    )
    preferred_property_type = MultiSelectField(choices=PROPERTY_TYPES_LIST, max_length=512)
    estimated_monthly_savings = models.FloatField()
    preferred_property_location = MultiSelectField(choices=LOCATIONS_LIST, max_length=512)
    housing_user_data_manager = HousingDataManager()

class HousingCalculateMgr(models.Manager):
    def retrieveHousingCalculateData(self, housingUserData):
        housingCalculate= self.get_queryset().filter(housingUserData=housingUserData)
        print(housingCalculate)
        housingCalculate = housingCalculate[0]
        return {
            "maxPropertyPrice": housingCalculate.maxPropertyPrice,
            "downPayment": housingCalculate.downPayment,
            "lumpSumPayment": housingCalculate.lumpSumPayment,
            "maxHomeLoan": housingCalculate.maxHomeLoan,
            "monthlyInstallment": housingCalculate.monthlyInstallment,
            "loanPeriod": housingCalculate.loanPeriod,
        }


    def createHousingCalculateData(self,housingUserData,maxPropertyPrice,downPayment,lumpSumPayment,maxHomeLoan,monthlyInstallment,loanPeriod):
        return self.create(housingUserData = housingUserData,
               maxPropertyPrice = maxPropertyPrice,
               downPayment = downPayment,
               lumpSumPayment = lumpSumPayment,
               maxHomeLoan = maxHomeLoan,
               monthlyInstallment = monthlyInstallment,
               loanPeriod = loanPeriod)

    def updateHousingCalculateData(self,housingUserData,maxPropertyPrice,downPayment,lumpSumPayment,maxHomeLoan,monthlyInstallment,loanPeriod):
        housingCalculate = self.get_queryset().filter(housingUserData=housingUserData)
        housingCalculate = housingCalculate[0]
        housingCalculate.maxPropertyPrice = maxPropertyPrice
        housingCalculate.downPayment = downPayment
        housingCalculate.lumpSumPayment = lumpSumPayment
        housingCalculate.maxHomeLoan = maxHomeLoan
        housingCalculate.monthlyInstallment = monthlyInstallment
        housingCalculate.loanPeriod = loanPeriod
        housingCalculate.save()



    

class HousingCalculate(models.Model):
    housingUserData = models.OneToOneField(HousingUserData, primary_key = True, on_delete=models.CASCADE)
    maxPropertyPrice = models.FloatField()
    downPayment = models.FloatField()
    lumpSumPayment = models.FloatField()
    maxHomeLoan = models.FloatField()
    monthlyInstallment = models.FloatField()
    loanPeriod = models.IntegerField()
    housingCalculateMgr = HousingCalculateMgr()


class ResaleFlatPrice(models.Model):
    location = models.CharField(max_length=32)
    flatType = models.CharField(max_length=32)
    propertyPrice = models.FloatField()
    resale_flat_price_manager = ResaleFlatPriceManager()
