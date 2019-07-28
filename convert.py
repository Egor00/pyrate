import datetime

import pandas as pd

from codes import is_crypto_code, is_common_code
from data_load import get_crypto_rates, get_common_rates, get_btc_rates


def _crypto2crypto_rates(from_currency_code, to_currency_code, from_date, to_date):
    if from_currency_code == to_currency_code:
        return [1] * (to_date - from_date).days
    from_currency_rates = pd.Series(get_crypto_rates(from_currency_code, from_date, to_date))
    to_currency_rates = pd.Series(get_crypto_rates(to_currency_code, from_date, to_date))
    rates = dict(from_currency_rates / to_currency_rates)
    return rates


def _common2common_rates(from_currency_code, to_currency_code, from_date, to_date):
    if from_currency_code == to_currency_code:
        return [1] * (to_date - from_date).days
    from_currency_rates = pd.Series(get_common_rates(from_currency_code, from_date, to_date))
    to_currency_rates = pd.Series(get_common_rates(to_currency_code, from_date, to_date))
    rates = dict(from_currency_rates / to_currency_rates)
    return rates


def _crypto2common_rates(from_currency_code, to_currency_code, from_date, to_date):
    from_currency_rates = pd.Series(get_crypto_rates(from_currency_code, from_date, to_date))
    to_currency_rates = pd.Series(get_common_rates(to_currency_code, from_date, to_date))
    btc_rates = pd.Series(get_btc_rates(from_date, to_date))
    usd_rates = pd.Series(get_common_rates('USD', from_date, to_date))
    rates = dict(from_currency_rates * btc_rates * usd_rates / to_currency_rates)
    return rates


def _common2crypto_rates(from_currency_code, to_currency_code, from_date, to_date):
    inverse_rates = pd.Series(_crypto2common_rates(to_currency_code, from_currency_code, from_date, to_date))
    rates = dict(1 / inverse_rates)
    return rates


def get_rates(from_currency_code: str, to_currency_code: str,
              from_date: datetime.date = datetime.date.today() - datetime.timedelta(days=1),
              to_date: datetime.date = datetime.date.today()):
    if is_crypto_code(from_currency_code):
        if is_crypto_code(to_currency_code):
            return _crypto2crypto_rates(from_currency_code, to_currency_code, from_date, to_date)
        elif is_common_code(to_currency_code):
            return _crypto2common_rates(from_currency_code, to_currency_code, from_date, to_date)
        else:
            raise ValueError('invalid currency code: %s' % to_currency_code)
    elif is_common_code(from_currency_code):
        if is_crypto_code(to_currency_code):
            return _common2crypto_rates(from_currency_code, to_currency_code, from_date, to_date)
        elif is_common_code(to_currency_code):
            return _common2common_rates(from_currency_code, to_currency_code, from_date, to_date)
        else:
            raise ValueError('invalid currency code: %s' % to_currency_code)
    else:
        raise ValueError('invalid currency code: %s' % from_currency_code)
