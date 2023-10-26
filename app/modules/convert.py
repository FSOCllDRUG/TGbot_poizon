import json


def convert_price(price):
    with open('app/data/data.json', 'r') as f:
        data = json.load(f)
    rate = data['rate']
    vikup = data['vikup']
    converted_price = price * rate * (1 + vikup / 100)
    return converted_price


def get_data():
    with open('app/data/data.json', 'r') as f:
        data = json.load(f)
    return data
