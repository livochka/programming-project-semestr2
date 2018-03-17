# Created to find values of hryvna exchange rate for the last month
import json
from urllib.request import urlopen
import calendar


def mid(l):
    """
    l: list with values og hryvna exchange rate
    return: middle value
    """
    return sum(l) / len(l)


def get_rate(year, month, day):
    """
    str, str, str -> tuple
    Getting hryvna exchange rate from NBU
    year, month, day: str date
    return: date, exchange rate
    """
    url = 'https://bank.gov.ua/NBUStatService/v1/statdirectory' \
          '/exchange?valcode=USD&date=' + year + month + day + '&json'
    info = urlopen(url).read().decode()

    try:
        info = json.loads(info)[0]
    except IndexError:
        # In case, when this page is not exist
        return None

    return info['exchangedate'], info['rate']


def generate_days(l):
    """
    Generating days for a specific month
    l: number of days in month
    return: list with str number of days
    """
    return [str(x) if x > 9 else '0' + str(x) for x in range(1, 32)]


def main(year, month):
    """
    int, int -> set, float
    year, month: date
    return: set with tuples(date, hryvna exchange rate), middle exchange value
    """
    length_month = calendar.monthrange(year, month)[1]
    days = generate_days(length_month)
    month = str(month) if month > 9 else '0' + str(month)
    rates = set()

    for day in days:
        rate = get_rate(str(year), month, day)
        if rate:
            rates.add(rate)

    # Getting middle value
    middle = mid(list(x[1] for x in rates))
    return rates, middle



if __name__ == '__main__':
    print(main(2017, 12))
