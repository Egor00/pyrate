import numpy as np
import matplotlib.pyplot as plt
from matplotlib import ticker


def plot(values: dict):
    if not values:
        return
    dates = np.array([date.strftime('%d.%m') for date in values])
    rates = np.array(list(values.values()))
    fig = plt.figure(1, figsize=(15, 5))
    plt.plot(dates, rates, c='b', mfc='k', marker='H')
    plt.tick_params(direction='inout', length=10)
    plt.grid()
    fig.axes[0].yaxis.set_major_locator(ticker.MultipleLocator((max(rates) - min(rates)) / 30))
    fig.axes[0].xaxis.set_major_locator(ticker.MultipleLocator(len(dates)//30 + 1))
    plt.show()
