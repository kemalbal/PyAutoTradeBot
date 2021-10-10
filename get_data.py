#%%
import config
import csv
import os
from binance import Client

data_folder_path = os.path.sep.join(['dataset','binance']) + os.path.sep
# client = Client(config.API_KEY, config.API_SECRET)
client = Client()

#%%
file_name = "2021_may_15minutes"
start_date ="2021-05-01"
end_date = "2021-05-31"

csvfile = open(data_folder_path + file_name + '.csv', 'w', newline='')
candlestick_writer = csv.writer(csvfile, delimiter=',')

# Open time
# Open
# High
# Low
# Close
# Volume
# Close time
# Quote asset volume
# Number of trades
# Taker buy base asset volume
# Taker buy quote asset volume
# Ignore.

candlesticks = client.get_historical_klines(
    "BTCUSDT", Client.KLINE_INTERVAL_15MINUTE, start_date, end_date)

for candlestick in candlesticks:
    candlestick[0] = candlestick[0] / 1000
    candlestick_writer.writerow(candlestick)

csvfile.close()

#%%
def gel_all_prices():
    prices = client.get_all_tickers()

    for price in prices:
        print(price)

# get_prices("2021-01-01", "2021-01-31", "2021_jan_15minutes")