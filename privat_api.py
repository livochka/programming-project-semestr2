# Module exist to get info from PrivatBank API

import urllib.request, urllib.parse, urllib.error
import json

url = 'https://api.privatbank.ua/p24api/'

# Exchange course for today: buy and sale
ex = urllib.request.urlopen(url + 'pubinfo?json&exchange&coursid=5')
data = ex.read().decode()

exchange = json.loads(data)[0]
exchange_sale = exchange['sale']
exchange_buy = exchange['buy']

print("Buy: {};  Sale: {}".format(str(exchange_buy), str(exchange_sale)))

# Exchange course for any date and any currency

date = '21.06.2011'
get_date = urllib.request.urlopen(url + 'exchange_rates?json&date=' + date)
data = get_date.read().decode()
data = json.loads(data)['exchangeRate']

print(data)

