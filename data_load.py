import datetime
import requests

from bs4 import BeautifulSoup


def get_common_rates(cur_code: str, from_date: datetime.date = datetime.date.today() - datetime.timedelta(days=1),
                     to_date: datetime.date = datetime.date.today()):
    """
    Downloads currency exchange rates against the ruble.
    """
    rates = {}
    cur_code = cur_code.upper()
    for day in range((to_date - from_date).days):
        rate_date = from_date + datetime.timedelta(days=day)
        if isinstance(rate_date, datetime.datetime):
            rate_date = rate_date.date()
        if cur_code == 'RUB':
            rate = 1
        else:
            rate = _get_cbr_rate(cur_code, rate_date)
        rates[rate_date] = rate
    return rates


def _get_cbr_rate(cur_code: str, date: datetime.date = datetime.date.today()):
    """
    Downloads exchange rates on the specified day from cbr.ru
    """
    url = 'http://www.cbr.ru/scripts/XML_daily_eng.asp'
    try:
        response = requests.get(url, timeout=5, params={'date_req': date.strftime('%d.%m.%Y')})
        if response.status_code != requests.codes.ok:
            response.raise_for_status()
    except (requests.exceptions.ConnectionError, requests.exceptions.HTTPError, requests.exceptions.ReadTimeout):
        raise ConnectionError('Can not get data from cbr.com')
    soup = BeautifulSoup(response.content, features='lxml-xml')
    node = list(filter(lambda x: x.CharCode.string == cur_code, soup.ValCurs.children))[0]
    value = float(node.Value.string.replace(',', '.'))
    nominal = float(node.Nominal.string.replace(',', '.'))
    rate = value / nominal
    return rate


def get_crypto_rates(cur_code: str, from_date: datetime.date = datetime.date.today() - datetime.timedelta(days=1),
                     to_date: datetime.date = datetime.date.today()):
    """
    Downloads currency exchange rates against BTC, using poloniex.com API.
    Raises ConnectionError if cannot get response or ValueError if poloniex return error
    """
    if cur_code == 'BTC':
        rates = {from_date + datetime.timedelta(days=i): 1 for i in range((to_date - from_date).days)}
        return rates
    poloniex_url = 'https://poloniex.com/public?'
    try:
        start_time = datetime.datetime.combine(from_date, datetime.time()).timestamp()
        end_time = datetime.datetime.combine(to_date, datetime.time()).timestamp()
        response = requests.get(poloniex_url, timeout=5, params={'command': 'returnChartData',
                                                                 'currencyPair': 'BTC_%s' % cur_code,
                                                                 'start': start_time,
                                                                 'end': end_time,
                                                                 'period': 86400}).json()  # 1 day = 86400 seconds
    except (requests.exceptions.ConnectionError, requests.exceptions.HTTPError, requests.exceptions.ReadTimeout):
        raise ConnectionError('Can not get data from poloniex.com')
    try:
        error = response['error']
    except (TypeError, KeyError):
        rates = {datetime.date.fromtimestamp(val['date']): val['weightedAverage'] for val in response}
    else:
        raise ValueError('poloniex.com returned error: %s' % error)
    return rates


def get_btc_rates(from_date: datetime.date = datetime.date.today() - datetime.timedelta(days=1),
                  to_date: datetime.date = datetime.date.today()):
    """
    Downloads BTC rates using coindesk.com API. Raises ConnectionError if cannot
    get response.
    """
    coindesk_url = 'https://api.coindesk.com/v1/bpi/historical/close.json'
    try:
        response = requests.get(coindesk_url, timeout=5, params={'start': from_date.strftime('%Y-%m-%d'),
                                                                 'end': to_date.strftime('%Y-%m-%d')}).json()
    except (requests.exceptions.ConnectionError, requests.exceptions.HTTPError, requests.exceptions.ReadTimeout) as e:
        raise ConnectionError('Can not get data from coindesk.com', e)
    rates = {datetime.datetime.strptime(date, '%Y-%m-%d').date(): response['bpi'][date] for date in response['bpi']}
    return rates
