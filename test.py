import requests
import json

data = requests.get('https://min-api.cryptocompare.com/data/price?fsym=DOGE&tsyms=USD')
jsons = json.loads(data.text)
price = float(jsons['USD']) * 1000000


print('${:,.2f}'.format(price))
