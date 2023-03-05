from io import TextIOWrapper
from typing import List

from urllib.request import urlopen, Request

import json

from uuid import uuid4

from datetime import datetime


def get_fields() -> List[str]:
    headers={'User-Agent': 'Mozilla/5.0'}
    url = 'https://data.gov.sg/api/action/datastore_search?resource_id=f1765b54-a209-4718-8d38-a39237f502b3'
    request = Request(url, headers=headers)
    fileobj = urlopen(request)
    data = json.loads(fileobj.read())['result']
    
    fields = []
    for field in data['fields']:
        fields.append(field['id'])

    return fields

def get_prices(file: TextIOWrapper, url: str, fields: List[str]) -> None:
    headers={'User-Agent': 'Mozilla/5.0'}

    while True:
        request = Request(f'https://data.gov.sg{url}', headers=headers)
        fileobj = urlopen(request)
        data = json.loads(fileobj.read())['result']

        records = data['records']

        if not records:
            break

        for record in records:
            row = ','.join([str(record[key]) for key in fields])
            file.write(row)
            file.write('\n')

        url = data['_links']['next']

def resale_flat_price(years: List[int]):
    fields = get_fields()
    now = datetime.now()
    formatted_date = now.strftime("%Y%m%d%H%M%S")
    filename = f"./resale_flat_price_{formatted_date}.csv"
    f = open(filename, "w")

    for year in years:
        get_prices(file=f, url=f"/api/action/datastore_search?q={year}&resource_id=f1765b54-a209-4718-8d38-a39237f502b3", fields=fields)
    
    f.close()

if __name__ == '__main__':
    resale_flat_price([2022, 2023])
    
