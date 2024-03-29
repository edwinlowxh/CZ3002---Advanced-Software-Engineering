import concurrent.futures

from urllib.request import urlopen, Request

from bs4 import BeautifulSoup, NavigableString, Tag

from uuid import uuid4

from datetime import datetime

import time


def scrape(start: int, end: int):
    car_details = []

    for i in range(start, end + 1):
        print(i)
        carCode = str(i)

        #Ensure that url does not redirect
        url = f"https://www.sgcarmart.com/new_cars/newcars_pricing.php?CarCode={str(i)}"
        hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'}
        request = Request(url, headers=hdr)
        response = urlopen(request)
        if response.getcode() == 429:
            time.sleep(int(response.response.getheader('Retry-After')))
            request = Request(url, headers=hdr)
            response = urlopen(request)

        if (response.geturl() != url):
            # print("redirect")
            continue

        page = BeautifulSoup(response, "html.parser")

        #Check if parallel imported
        parallel_import = False
        title = page.find("a", {"class": "nounderline globaltitle"})
        for tag in title:
            if "Parallel Imported" in tag.text:
                parallel_import = True
                break

        if parallel_import:
            continue

        #Get Make
        text_navigation = page.find("div", {"id": "text_navigation"})
        for tag in text_navigation:
            if isinstance(tag, Tag):
                if "newcars_listing.php?MOD=" in tag['href']:
                    car_make = (tag.text)
                elif "newcars_overview.php?CarCode" in tag['href']:
                    model_name = (tag.text)

        model_name.replace(f'{car_make} ', '')

        content740 = page.find("div", {"class": "content740"})
        newboxborders = content740.find_all("div", {"class": "newboxborder"}, recursive=False)

        try:
            tablerows = newboxborders[0].find("table").find_all("tr", recursive=False)
        except AttributeError:
            continue

        cells = []      #Contains the information for the different models
        for i in range(len(tablerows)):
            if i % 2 == 0:
                cells.extend(tablerows[i].find_all("td", {"valign": "top"}, recursive=False))       #Split row into individual model cell and add to array

        relevant_rows = {"Spec Name": 1, "Current Price": 3, "Depreciation": 4, "Down Payment": 5,
                        "Installment": 6, "COE": 7, "Road Tax": 8, "OMV": 9, "ARF": 10, "VES": 11}

        for cell in cells:
            cellrows = cell.find("table").find_all("tr", recursive=False)

            #Spec name
            spec_name = cellrows[relevant_rows["Spec Name"]].find("a").text
            href = cellrows[relevant_rows["Spec Name"]].find("a")['href']
            subCode = href[href.index("Subcode=") + 8:]
            # print(spec_name)

            # Current Price
            try:
                current_price = cellrows[relevant_rows["Current Price"]].find("span").text
                coe_incl = str(True)
                if "w/o COE" in cellrows[relevant_rows["Current Price"]].find_all("td", recursive=False)[2].text:
                    coe_incl = str(False)
            except AttributeError:
                current_price = "POA"
            # print(current_price)

            #Depreciation
            depreciation = cellrows[relevant_rows["Depreciation"]].find_all("td", recursive=False)[2].text.lstrip().rstrip()
            # depreciation = ''.join(i for i in depreciation if i.isdigit())
            # print(depreciation)

            #Down payment
            down_payment = cellrows[relevant_rows["Down Payment"]].find_all("td", recursive=False)[2].text.lstrip().rstrip()
            # print(down_payment)

            #Installment
            installment = cellrows[relevant_rows["Installment"]].find_all("td", recursive=False)[2].text.lstrip().rstrip()
            # print(installment)

            #COE
            coe = cellrows[relevant_rows["COE"]].find_all("td", recursive=False)[2].text.lstrip().rstrip()
            # print(coe)

            #Road Tax
            road_tax = cellrows[relevant_rows["Road Tax"]].find_all("td", recursive=False)[2].text.lstrip().rstrip()
            # print(road_tax)

            #OMV
            omv = cellrows[relevant_rows["OMV"]].find_all("td", recursive=False)[2].text.lstrip().rstrip()
            # print(omv)

            #ARF
            arf = cellrows[relevant_rows["ARF"]].find_all("td", recursive=False)[2].text.lstrip().rstrip()
            # print(arf)

            #ves
            # ves = cellrows[relevant_rows["VES"]].find_all("td", recursive=False)[2].text.lstrip().rstrip()
            # print(ves)

            # print()

            skip = False
            fuelType = "-"
            fuelEconomy = "-"

            # f"https://www.sgcarmart.com/new_cars/newcars_specs.php?CarCode={str(carCode)}&Subcode={str(subCode)}"
            url = f"https://www.sgcarmart.com/new_cars/newcars_specs.php?CarCode={str(carCode)}&Subcode={str(subCode)}"
            request = Request(url, headers=hdr)
            response = urlopen(request)

            if response.getcode() == 429:
                time.sleep(int(response.getheader("Retry-After")))
                request = Request(url, headers=hdr)
                response = urlopen(request)

            if (response.geturl() != url):
                skip = True

            page = BeautifulSoup(response, "html.parser")

            if not skip:
                table = page.find("table", id='submodel_spec').find_all('tr', recursive=False)

                #Get fuel type
                fuelType = table[3].find_all("td", recursive=False)[1].text
                if ("Nickel" in fuelType or "Lithium-ion" in fuelType or fuelType == "unknown"):
                    fuelType = table[4].find_all("td", recursive=False)[1].text
                # print(fuelType)

                #Get fuel economy
                if fuelType == "Electric":
                    try:
                        fuelEconomy = table[11].find_all("td", recursive=False)[1].text[:table[11].find_all("td", recursive=False)[1].text.index("kWh")]
                    except ValueError:
                        pass
                elif "Petrol-Electric" in fuelType or "Diesel-Electric" in fuelType:
                    fuelEconomy = table[13].find_all("td", recursive=False)[1].text
                else:
                    fuelEconomy = table[10].find_all("td", recursive=False)[1].text
                # print(fuelEconomy)

            input_values = [carCode, subCode, car_make, model_name, spec_name, current_price, depreciation, down_payment, installment, coe,
                            road_tax, omv, arf, fuelEconomy, fuelType, coe_incl]

            for i in range(5,14):
                if (input_values[i] != '-' and input_values[i] != "POA"):
                    input_values[i] = ''.join(x for x in input_values[i][:10] if (x.isdigit() or x == '.'))       #Get integer only
            # print(input_values)

        car_details.append(input_values)
        time.sleep(1)
    
    return car_details   


if __name__ == '__main__':
    argument_intervals = [(21000, 22000)]
    total_indexes = 0
    for start, end in argument_intervals:
        total_indexes += end - start
    equal_interval = total_indexes // 3

    intervals = []
    for start, end in argument_intervals:
        while start <= end:
            intervals.append((start, min(start + equal_interval, end)))
            start += equal_interval
    print(intervals)

    now = datetime.now()
    formatted_date = now.strftime("%Y%m%d%H%M%S")
    filename = f"./price_list/car_price_{formatted_date}.csv"
    f = open(filename, "w")

    # Write header
    f.write(str("car_code,sub_code,make,model,spec,current_price,depreciation,down_payment,installment,coe,road_tax,omv,arf,fuel_economy,fuel_type,coe_incl\n"))

    car_details = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        for result in executor.map(lambda p: scrape(*p), intervals):
            car_details.extend(result)

    for car_detail in car_details:
        f.write(','.join(car_detail))
        f.write('\n')
        f.close()
