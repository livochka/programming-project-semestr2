# Module created to get information from National Bank of Ukraine

import urllib.request, urllib.parse, urllib.error
import json


url = 'https://bank.gov.ua/NBUStatService/v1/statdirectory/inflation?period=m' \
      '&date='

# Getting consumer price index (CPI) for 2013 and 2015 years in Lvivska obl

date_1 = '201201&json'
date_2 = '201501&json'

ex_1 = urllib.request.urlopen(url + date_1)
ex_2 = urllib.request.urlopen(url + date_2)

data_1 = ex_1.read().decode()
data_2 = ex_2.read().decode()

Lvivska_obl = []

year_1 = json.loads(data_1)
year_2 = json.loads(data_2)

# Adding of info with value 'Total' on key 'mcrd081'
# what means that this is CPI and value '13' on key 'ku'
# what means that this is about Lvivska oblast

for x in year_1:
    if x['mcrd081'] == 'Total' and x['ku'] == '13' and x['tzep'] == 'DTPY_':
        Lvivska_obl.append([x['dt'], x['value']])

for x in year_2:
    if x['mcrd081'] == 'Total' and x['ku'] == '13' and x['tzep'] == 'DTPY_':
        Lvivska_obl.append([x['dt'], x['value']])

print(Lvivska_obl)