# r = get_statistic('AMD', from_date=datetime.now()-timedelta(days=30))
# for dat in r:
#   print("%s: %s" % (dat.strftime("%d/%m/%y"), r[dat]))

# plot(get_statistic('USD', 'EUR'))

# print(get_data_cbrf('Eth'))

# b = get_codes()


# print(get_btc_rates(datetime.now() - timedelta(days=10)))
# from rates import get_codes, get_crypto_rates, get_common_rates

'''a = get_data_crypto('ETH', from_date=datetime.now()-timedelta(days=10))
prev = 0
for b in a:
    print('%s : %s' % (b, a[b] - prev))
    prev = a[b]'''
import datetime
import plot
import pandas as pd

from codes import get_codes, is_crypto_code, is_common_code
from convert import _crypto2common_rates, get_rates
from data_load import get_crypto_rates, get_common_rates, get_btc_rates

# start_date = datetime.datetime.strptime('01.03.2019', '%d.%m.%Y').date()
# end_date = datetime.date.today()
# a = get_rates('BYN',  'BTC', from_date=start_date,
#                to_date=end_date)
# a = _common2crypto_rates('BYN', 'BTC', from_date=start_date, to_date=end_date)
# a = _crypto2common_rates('BTC', 'BYN', from_date=start_date, to_date=end_date)
'''btcr = pd.Series(get_crypto_rates('BTC', start_date, end_date))
byn = pd.Series(get_common_rates('BYN', start_date, end_date))
btc = pd.Series(get_btc_rates(start_date, end_date))
usd = pd.Series(get_common_rates('USD', start_date, end_date))
frame = pd.DataFrame({'btcr': btcr, 'byn': byn, 'btc': btc, 'usd': usd})'''
# print(type(a))
# plot.plot(a)
# print(frame)
print(is_common_code('USD'))
