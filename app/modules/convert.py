import json


def convert_price(price):
    with open('app/data/data.json', 'r') as f:
        data = json.load(f)
    rate = data['rate']
    converted_price = price * rate * 1.05
    return converted_price


def get_data():
    with open('app/data/data.json', 'r') as f:
        data = json.load(f)
    return data
