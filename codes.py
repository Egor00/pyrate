import csv
import os
import re

import requests
from bs4 import BeautifulSoup


_codes_file_name = os.path.join('codes', '%s_codes.csv')
_crypto_codes_file_name = _codes_file_name % 'crypto'
_common_codes_file_name = _codes_file_name % 'common'


def _load_codes():
    """
    Loads regular and crypto currency codes. Uses cbr.ru for regular currencies
    and poloniex.com for crypto. Raises ConnectionError if cannot get response
    from the above resources.
    """
    cbr_url = 'http://www.cbr.ru/scripts/XML_daily_eng.asp'
    poloniex_url = 'https://poloniex.com/public?'
    try:
        response = requests.get(cbr_url, timeout=5)
    except Exception:
        raise ConnectionError('Can not get data from cbr.com')
    soup = BeautifulSoup(response.content, features='lxml-xml')
    common_cur_codes = {node.CharCode.string: node.Name.string for node in soup.ValCurs.children}
    common_cur_codes['RUB'] = 'Russian Ruble'
    try:
        response = requests.get(poloniex_url, timeout=5, params={'command': 'returnCurrencies'}).json()
    except Exception:
        raise ConnectionError('Can not get data from poloniex.com')
    crypto_cur_codes = {cur: response[cur]['name'] for cur in response}
    codes = {'common': common_cur_codes, 'crypto': crypto_cur_codes}
    return codes


def _save_codes(cur_codes):
    """
    Creates, if necessary, the 'codes' folder where CSV files with code-currency
    pairs are saved
    """
    dir_name = os.path.dirname(_common_codes_file_name)
    if not os.path.isdir(dir_name):
        os.mkdir(dir_name)
    crypto_cur_codes = cur_codes['crypto'].items()
    common_cur_codes = cur_codes['common'].items()

    with open(_crypto_codes_file_name, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(crypto_cur_codes)
    with open(_common_codes_file_name, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(common_cur_codes)


def get_codes():
    """
    Uploads a code-currency pairs from files, if they exist, otherwise
    downloads and saves pairs, using _load_codes and _save_codes functions
    """
    if not (os.path.isfile(_common_codes_file_name) and os.path.isfile(_crypto_codes_file_name)):
        codes = _load_codes()
        _save_codes(codes)
        return codes
    with open(_common_codes_file_name, 'r', newline='') as file:
        reader = csv.reader(file)
        common_cur_codes = {row[0]: row[1] for row in reader}
    with open(_crypto_codes_file_name, 'r', newline='') as file:
        reader = csv.reader(file)
        crypto_cur_codes = {row[0]: row[1] for row in reader}
    cur_codes = {'common': common_cur_codes, 'crypto': crypto_cur_codes}
    return cur_codes


def _is_some_code(code, cur_type):
    """
    Checks whether the code is a crypto or regular currency code.
    """
    if not (os.path.isfile(_common_codes_file_name) and os.path.isfile(_crypto_codes_file_name)):
        cur_codes = _load_codes()
        _save_codes(cur_codes)
        return code in cur_codes['common'].update(cur_codes['crypto'])
    with open(_codes_file_name % cur_type) as file:
        for line in file:
            if re.match(r'\b%s,' % code, line) is not None:
                return True
    return False


def is_common_code(code):
    """
    Checks whether the code is a regular currency code.
    """
    return _is_some_code(code, 'common')


def is_crypto_code(code):
    """
    Checks whether the code is a crypto currency code.
    """
    return _is_some_code(code, 'crypto')
