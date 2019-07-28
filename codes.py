import csv
import os
import re

import requests
from bs4 import BeautifulSoup


_some_codes_file_name = 'codes/%s_codes.csv'
_crypto_codes_file_name = _some_codes_file_name % 'crypto'
_common_codes_file_name = _some_codes_file_name % 'common'


def _load_codes() -> dict:
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
    cur_codes = {'common': common_cur_codes, 'crypto': crypto_cur_codes}
    return cur_codes


def _write_codes(cur_codes: dict):
    dir_name = os.path.dirname(_common_codes_file_name)
    if not os.path.isdir(dir_name):
        os.mkdir(dir_name)
    crypto_cur_codes = [[code, name] for (code, name) in cur_codes['crypto'].items()]
    common_cur_codes = [[code, name] for (code, name) in cur_codes['common'].items()]
    with open(_crypto_codes_file_name, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(crypto_cur_codes)
    with open(_common_codes_file_name, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(common_cur_codes)


def get_codes() -> dict:
    if not (os.path.isfile(_common_codes_file_name) and os.path.isfile(_crypto_codes_file_name)):
        cur_codes = _load_codes()
        _write_codes(cur_codes)
        return cur_codes
    with open(_common_codes_file_name, 'r', newline='') as file:
        reader = csv.reader(file)
        common_cur_codes = {row[0]: row[1] for row in reader}
    with open(_crypto_codes_file_name, 'r', newline='') as file:
        reader = csv.reader(file)
        crypto_cur_codes = {row[0]: row[1] for row in reader}
    cur_codes = {'common': common_cur_codes, 'crypto': crypto_cur_codes}
    return cur_codes


def _is_some_code(code: str, cur_type: str):
    if not (os.path.isfile(_common_codes_file_name) and os.path.isfile(_crypto_codes_file_name)):
        cur_codes = _load_codes()
        _write_codes(cur_codes)
        return code in cur_codes['common'].append(cur_codes['crypto'])
    with open(_some_codes_file_name % cur_type) as file:
        for a in file:
            if re.match(r'\b%s,' % code, a) is not None:
                return True
    return False


def is_common_code(code: str):
    return _is_some_code(code, 'common')


def is_crypto_code(code: str):
    return _is_some_code(code, 'crypto')
