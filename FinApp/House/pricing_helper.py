from .constants import (
    ANNUAL_INTEREST_RATE,
    HDB_DOWN_PAYMENT_RATE,
    LOAN_PERIOD,
    MAX_LTV_RATE
)

def calculate_max_home_loan(monthly_installment: float) -> float:
    monthly_interest_rate = ANNUAL_INTEREST_RATE / 12

    return monthly_installment * (((1 + monthly_interest_rate) ** (LOAN_PERIOD *12)-1) /
                                                  (monthly_interest_rate * (1 + monthly_interest_rate)**(LOAN_PERIOD * 12)))


#TODO: Verify accuracy of option fee based on property types
def calculate_option_fee(property_types: list[str]) -> int:
    if "4 ROOM" or "5 ROOM" or "EXECUTIVE" or "MULTI-GENERATION" in property_types:
        optionFee = 2000
    elif "3 ROOM" in property_types:
        optionFee = 1000
    else:
        optionFee = 500
    
    return optionFee

#TODO: Verify accuracy of formula
def calculate_stamp_duty(max_property_price: float) -> float:
    # 1% first 180k, 2% next 180k, 3% next 640k, 4% remaining
    if max_property_price < 180000:
        stamp_duty = 0.01 * max_property_price
    else:
        stamp_duty = 0.01 * 180000
        remainingPropertyPrice = max_property_price - 180000
        if(remainingPropertyPrice < 180000):
            stamp_duty += 0.02 * remainingPropertyPrice
        else:
            stamp_duty += 0.02 * 180000
            remainingPropertyPrice -= 180000
            if (remainingPropertyPrice < 640000):
                stamp_duty += 0.03 * remainingPropertyPrice
            else:
                stamp_duty += 0.03 * 640000
                remainingPropertyPrice -= 640000
                stamp_duty += 0.04 * remainingPropertyPrice

    return stamp_duty

def calculate_max_LTV(property_price: float) -> float:
    return MAX_LTV_RATE * property_price

def calculate_monthly_installment(max_LTV: float, period: int) -> float:
    period *= 12
    monthly_interest_rate = ANNUAL_INTEREST_RATE / 12
    return (max_LTV * (monthly_interest_rate * (1 + monthly_interest_rate) ** period) /
                                          ((1 + monthly_interest_rate) ** period - 1))

def calculate_down_payment(property_price: float) -> float:
    return HDB_DOWN_PAYMENT_RATE * property_price