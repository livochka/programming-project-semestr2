# Created to get information from World Bank API

import wbdata


# All available topics

available_info = wbdata.get_source()
for x in available_info:
    print(x['id'], x['name'])

# Information about G20 Financial Inclusion Indicators

inclusion_indicators = wbdata.get_indicator(source=33)
print(inclusion_indicators)

# Information 'The consumer price index reflects the
# change in prices for the average consumer of a constant basket of consumer
# goods. Data is in nominal terms and seasonally adjusted.' for USA for all
# years.

cpi = wbdata.get_data('CPTOTSAXN',  country='USA')
print(cpi)

