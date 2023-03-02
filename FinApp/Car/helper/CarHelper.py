from Car.models import Car, Trip

def calc_cost(car: Car, mileage: float):
        #10 year period
        insurance = 17500 #Assuming average
        servicing = 10000 #Assuming average
        installment = car.installment * 12 * 10
        road_tax = car.road_tax * 10
        remaining_value = car.current_price - 10 * car.depreciation
        fuel_cost = 0

        
        fuel_type = car.fuel_type

        if ('Petrol' in fuel_type):
            fuel_type = 'Petrol'
        elif ('Diesel' in fuel_type):
            fuel_type = 'Diesel'
        else:
            fuel_type = 'Electricity'

        fuel_economy = car.fuel_economy

        if fuel_economy == None:
            fuel_economy = 9.7   #Based on survey average
        mileage = mileage / 1000      #Mileage in terms of KM
        # fuelPrice = Fuel.objects.get(fuelType=fuelType).fuelPrice
        fuel_price = 3
        fuel_cost = fuel_price * (mileage / 100 * fuel_economy) * 12 * 10

        total_cost = (insurance + servicing + installment + road_tax + fuel_cost - remaining_value) / (12 * 10)
        return total_cost