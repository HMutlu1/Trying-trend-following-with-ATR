import pandas as pd
import numpy as np
import yfinance as yf
import math
import matplotlib.pyplot as plt
def Supertrend(df, atr_period=10, multiplier=3):

    high, low, close = df['High'], df['Low'], df['Adj Close']

    true_range = pd.concat([high - low, high - close.shift(), close.shift() - low], axis=1).abs().max(axis=1)
    average_true_range = true_range.ewm(alpha=1/atr_period, min_periods=atr_period).mean()
    df['ATR'] = average_true_range

    hl2 = (high + low) / 2

    upper_band = hl2 + (multiplier * average_true_range)
    lower_band = hl2 - (multiplier * average_true_range)

    supertrend = pd.Series(True, index=df.index)

    for i in range(1, len(df.index)):
        if close.iloc[i] > upper_band.iloc[i-1]:
            supertrend.iloc[i] = True

        elif close.iloc[i] < lower_band.iloc[i-1]:
            supertrend.iloc[i] = False

        else:
            supertrend.iloc[i] = supertrend.iloc[i-1]

           
            if supertrend.iloc[i] and lower_band.iloc[i] < lower_band.iloc[i-1]:
                lower_band.iloc[i] = lower_band.iloc[i-1]
            if not supertrend.iloc[i] and upper_band.iloc[i] > upper_band.iloc[i-1]:
                upper_band.iloc[i] = upper_band.iloc[i-1]

        upper_band.iloc[i] = np.nan if supertrend.iloc[i] else upper_band.iloc[i]
        lower_band.iloc[i] = np.nan if not supertrend.iloc[i] else lower_band.iloc[i]

    result_df = pd.DataFrame({'Supertrend': supertrend, 'Lowerband': lower_band, 'Upperband': upper_band}, index=df.index)

    return result_df

symbol = 'the stock you chose'
df = yf.download(symbol, start='2022-01-01')

supertrend = Supertrend(df)
df = df.join(supertrend)

plt.figure(figsize=(12,12))

plt.subplot(2, 1, 1)
plt.plot(df['Adj Close'], label='Close Price')
plt.plot(df['Lowerband'], color='green', label='Lowerband')
plt.plot(df['Upperband'], color='red', label='Upperband')
plt.legend()

plt.subplot(2, 1, 2)
plt.plot(df['ATR'], color='purple', label='ATR')
plt.legend()

plt.suptitle(f'Supertrend Analysis for {symbol} (For Educational Purposes Only)', fontsize=16, y=0.95)

plt.show()
