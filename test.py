import requests

url = "https://api.exchange.coinbase.com/products/BTCEUR"

headers = {"Accept": "application/json"}

response = requests.get(url, headers=headers)

print(response.text)