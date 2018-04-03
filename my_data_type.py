import calendar
from datetime import date
import json
from urllib.request import urlopen
import matplotlib.pyplot as plt


class AvailableCurrencies:
    """
    Represents all available currencies
    """
    UAN = 'UAN'
    USD = 'USD'
    RUB = 'RUB'
    EUR = 'EUR'


class UnavailableCurrencyError(Exception):
    pass


class NotGeneratedYetError(Exception):
    pass


class IncorrectDateError(Exception):
    pass


class IncorrectPlotType(Exception):
    pass


class ExchangeSample:
    """
    Created to represent currency exchange sample
    """

    MONTHS = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10',
              '11', '12']

    def __init__(self, currency):
        self._check_currency(currency)
        self.currency = currency
        self.currency2 = None
        self.year = None
        self.changes = {}

    @staticmethod
    def _check_currency(currency):
        """
        Checking whether input currency is available
        currency: currency we want to check
        return: none, raises UnavailableCurrencyError if currency is not
        available
        """
        if currency not in (AvailableCurrencies.UAN, AvailableCurrencies.USD,
                            AvailableCurrencies.RUB, AvailableCurrencies.EUR):
            raise UnavailableCurrencyError

    @staticmethod
    def _check_year(year):
        """
        Checking whether input year is correct
        year: input year
        return: None, raises IncorrectDateError if year is not correct
        """
        if not (2000 <= int(year) <= date.today().year):
            raise IncorrectDateError

    @staticmethod
    def middle_value(values):
        """
        Finds the middle value of the sample
        values: sample with numerical values
        return: the middle value in values
        """
        return sum(values) / len(values)

    def _source(self, currency, day, month, year):
        """
        Abstract method
        currency: currency information about you want to get
        day, month, year: date
        return: currency rate in this date
        """
        raise NotImplementedError

    def generate(self, currency2, year):
        """
        Generates information about changes in currency2 to self.currency in
        specific year
        currency2: the second currency to comparing self.currency with
        year: year of getting changes in exchange rate
        """
        self._check_currency(currency2)
        self._check_year(year)
        for month in self.MONTHS:

            # Getting for each month

            month_info = {month: {}}
            length = calendar.monthrange(int(year), int(month))

            for day in range(1, length[1] + 1):

                # Getting for each day

                day = str(day) if day > 9 else '0' + str(day)
                try:
                    month_info[month].update(self._source(day, month, year,
                                                          currency2))
                except TypeError:
                    continue

            self.changes.update(month_info)
        self.year = year
        self.currency2 = currency2

    def _plot(self, x, y, view, title='', xl='Months', bins=12):
        """
        Creates plot or hist with input parameters
        x: information for x-axis
        y: information for y-axis
        view: could be 'hist' or 'timeline'
        title: the title of the plot
        xl: x-axis label
        bins: number of separates for hist
        """
        if view not in {'hist', 'timeline'}:
            raise IncorrectPlotType('Must be hist or timeline')
        if view == 'hist':
            yl, xl = 'Frequency of occurrence', 'Value of exchange rate'
            plt.hist(y, bins=bins, density=False, stacked=True)
        else:
            yl = '{} exchange rate'.format(self.currency)
            plt.plot(x, y)

        # Additional information on plot or hist
        plt.title(title)
        plt.xlabel(xl)
        plt.ylabel(yl)

        plt.show()

    def year_information(self, view):
        """
        Getting information about specific year as plot
        view: type of plot - 'hist' or 'timeline'
        """
        try:
            months = self.changes.keys()
            values = [self.middle_value(self.changes[x].values()) for x in
                      self.changes]
            title = 'Information about {} to {} exchange rate in {} ' \
                    'year'.format(self.currency, self.currency2, self.year)
            self._plot(months, values, view, title)
        except KeyError:
            raise NotGeneratedYetError('Please, call object.generate(year) '
                                       'first')

    def half_year_information(self, part, view):
        """
        Getting information about specific part of the year as plot
        part: the first half of the year ('I') or the second half of the
        year('II')
        view: type of plot - 'hist' or 'timeline'
        """
        try:
            if part not in {'I', 'II'}:
                raise IncorrectDateError('Part of the year must be I or II')
            if part == 'I':
                month = self.MONTHS[0:6]
            else:
                month = self.MONTHS[6::]

            title = 'Information about {} to {} exchange rate in the {} ' \
                    'half of the {} year'.format(self.currency, self.currency2,
                                                 part, self.year)
            values = [self.middle_value(self.changes[x].values()) for x in
                      month]
            self._plot(month, values, view, title, bins=6)
        except KeyError:
            raise NotGeneratedYetError('Please, call object.generate(year) '
                                       'first')

    def month_information(self, month, view):
        """
        Getting information about input month of the self.year as plot
        month: number of the month, for example '03' for March
        view: type of plot - 'hist' or 'timeline'
        """
        try:
            if month not in self.MONTHS:
                raise IncorrectDateError
            days = [x[0:2] for x in self.changes[month].keys()]
            values = self.changes[month].values()

            # Additional information about plot
            title = 'Information about {} to {} exchange ' \
                    'rate as of {}.{}'.format(self.currency, self.currency2,
                                              month, self.year)
            xl = 'Days of the {}.{}'.format(month, self.year)
            self._plot(days, values, view, title, xl=xl)
        except KeyError:
            raise NotGeneratedYetError('Please, call object.generate(year) '
                                       'first')


class HryvnaExchange(ExchangeSample):
    """
    Created to analyse hryvna change exchange rate with information from NBU
    """

    def __init__(self):
        super().__init__(AvailableCurrencies.UAN)

    def _source(self, day, month, year, currency):
        """
        Provides GET-request to NBU to get hryvna exchange rate for date
        day, month, year: date
        currency: currency you want to get hryvna exchange rate for
        """

        url = 'https://bank.gov.ua/NBUStatService/v1/statdirectory' \
              '/exchange?valcode=' + currency + '&date=' + year + month + day + \
              '&json'
        info = urlopen(url).read().decode()

        try:
            info = json.loads(info)[0]
        except IndexError:
            # In case, when this page is not exist
            return None

        return {info['exchangedate']: info['rate']}


if __name__ == '__main__':
    my = HryvnaExchange()
    my.generate('USD', '2000')
    print(my.changes)
    my.half_year_information('I', 'hist')
