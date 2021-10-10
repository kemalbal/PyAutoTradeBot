from flask import Flask, render_template, request, flash, redirect, jsonify
import config
import csv
import numpy as np
import talib, backtest
from binance.client import Client
from binance.enums import *

app = Flask(__name__,
            static_url_path='',
            static_folder='static',
            template_folder='templates')

app.secret_key = b'trader_v1'

client = Client(config.API_KEY, config.API_SECRET)

@app.route('/')
def index():
    title = 'Trader'
    return render_template('index.html', title=title)


@app.route('/history')
def history():
    processed_candlesticks = []
    with open('data/2021_15minutes.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',',)
        for data in reader:
            candlestick = {
                "time": float(data[0]) / 1000,
                "open": float(data[1]),
                "high": float(data[2]),
                "low": float(data[3]),
                "close": float(data[4])
            }
            processed_candlesticks.append(candlestick)
    return jsonify(processed_candlesticks)

@app.route('/signal')
def signal():
    amount = 1000
    in_position = False
    coin_amount = 0
    position_coin_price = 0

    data = np.genfromtxt('data/2021_15minutes.csv', delimiter=',')
    time = data[:, 0]
    close = data[:, 4]
    rsi = talib.RSI(close, timeperiod=14)
    # rsi = rsi[~np.isnan(rsi)]

    # mavi, kırmızı
    stochrsif, stochrsis = talib.STOCH(rsi, rsi, rsi, fastk_period=14, slowk_period=3, slowd_period=3)

    signal_array = []
    
    stop = 1 - 0.05
    stop_count = 0

    for i in range(0, len(stochrsif)):
        if(position_coin_price > 0):
            if(position_coin_price * stop >= float(close[i])):
                if(in_position):
                    in_position = False
                    amount = coin_amount * float(close[i])
                    stop_count = stop_count + 1
                    signal_data = {
                                "time": float(time[i]) / 1000,
                                "position": 'belowBar',
                                "color": 'red',
                                "shape": 'arrowUp',
                                "text": 'STOP' + ' [' + str(amount) + ' - ' + str(position_coin_price / float(close[i])) + ']',
                                "size": 2
                            }
                    signal_array.append(signal_data)
                    continue

        if(float(stochrsif[i]) <= 30):
            if(float(stochrsif[i]) - float(stochrsis[i]) >= 0.1 and float(stochrsif[i]) - float(stochrsis[i]) <= 1):
                if(not in_position):
                    in_position = True
                    position_coin_price = float(close[i])
                    coin_amount = amount / float(close[i])
                    signal_data = {
                            "time": float(time[i]) / 1000,
                            "position": 'belowBar',
                            "color": 'green',
                            "shape": 'arrowUp',
                            "text": 'BUY' + ' [' + str(amount) + ']',
                            "size": 2
                        }
                    signal_array.append(signal_data)
        if(float(stochrsif[i]) >= 95):
            if(float(stochrsif[i]) - float(stochrsis[i]) <= -0.1 and float(stochrsif[i]) - float(stochrsis[i]) >= -1):
                if(in_position):
                    in_position = False
                    amount = coin_amount * float(close[i])
                    position_coin_price = 0
                    signal_data = {
                            "time": float(time[i]) / 1000,
                            "position": 'aboveBar',
                            "color": 'red',
                            "shape": 'arrowDown',
                            "text": 'SELL' + ' [' + str(amount) + ']',
                            "size": 2
                        }
                    signal_array.append(signal_data)

    # print(stop_count)
    return jsonify(signal_array)
# def signal():
#     amount = 1000
#     in_position = False
#     coin_amount = 0

#     data = np.genfromtxt('data/2021_15minutes.csv', delimiter=',')
#     time = data[:, 0]
#     close = data[:, 4]
#     rsi = talib.RSI(close)

#     signal_array = []
    
#     for i, rsi_value in enumerate(rsi):
#         rsi_value = float(rsi_value)
#         if(not np.isnan(rsi_value)):
#             if(rsi_value <= 30):
#                 if(not in_position):
#                     in_position = True
#                     coin_amount = amount / float(close[i])
#                     signal_data = {
#                             "time": float(time[i]) / 1000,
#                             "position": 'belowBar',
#                             "color": 'green',
#                             "shape": 'arrowUp',
#                             "text": 'BUY' + ' [' + str(amount) + ']',
#                             "size": 2
#                         }
#                     signal_array.append(signal_data)
#             if(rsi_value >= 70):
#                 if(in_position):
#                     in_position = False
#                     amount = coin_amount * float(close[i])
#                     signal_data = {
#                             "time": float(time[i]) / 1000,
#                             "position": 'aboveBar',
#                             "color": 'red',
#                             "shape": 'arrowDown',
#                             "text": 'SELL' + ' [' + str(amount) + ']',
#                             "size": 2
#                         }
#                     signal_array.append(signal_data)

#     return jsonify(signal_array)

@app.route('/rsi')
def rsi():
    data = np.genfromtxt('data/2021_15minutes.csv', delimiter=',')
    time = data[:, 0]
    close = data[:, 4]
    # rsi = talib.RSI(close)

    all_rsi_values = []
    for i, rsi_value in enumerate(rsi):
        rsi_value = float(rsi_value)
        if(not np.isnan(rsi_value)):
            rsi_data = {
                "time": float(time[i]) / 1000,
                "value": rsi_value
            }
            all_rsi_values.append(rsi_data)
    # print(all_rsi_values[0])
    return jsonify(all_rsi_values)
# rsi()