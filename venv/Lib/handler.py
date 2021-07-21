import requests

def lambda_handler(event=None,context=None):
    base_url = "https://api.gemini.com/v1"
    response = requests.get(base_url + "/pricefeed")
    prices = response.json()
    print(prices)

lambda_handler()
