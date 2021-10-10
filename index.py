# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, flash, redirect, jsonify
import config
import csv,json
import numpy as np
import talib
from backtest import Backtest
from strategies.Strategy import Strategy
from flask import Response
from datetime import datetime

from strategies.RSIStrategy import RSIStrategy
from strategies.RSIDStrategy import RSIDStrategy
from strategies.HODLStrategy import HODLStrategy
from strategies.MACDStrategy import MACDStrategy

app = Flask(__name__,
            static_url_path='',
            static_folder='static',
            template_folder='templates')

app.secret_key = b'trader_v1'

@app.route('/')
def index():
    title = 'Trader'
    return render_template('index.html', title=title)


@app.route('/history')
def history():
    processed_candlesticks = []
    with open('dataset/binance/2021_may_15minutes.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',',)
        # processed_candlesticks.append('Date,Open,High,Low,Close,Volume')
        for data in reader:
            candlestick = {
                # "time": datetime.utcfromtimestamp(float(data[0])).strftime('%Y-%m-%d %H:%M:%S'),
                "time": float(data[0]) / 1000,
                "open": float(data[1]),
                "high": float(data[2]),
                "low": float(data[3]),
                "close": float(data[4])
            }
            # date = datetime.utcfromtimestamp(float(data[0])).strftime('%Y-%m-%d %H:%M:%S')
            # candlestick = ','.join([date, data[1], data[2], data[3], data[4], data[5]])
            processed_candlesticks.append(candlestick)
    # return "\n".join(processed_candlesticks)
    return jsonify(processed_candlesticks)


@app.route('/trade')
def trade():
    backtest = Backtest()
    backtest.setData('2021_may_15minutes')

    # newStrategy = RSIStrategy()
    # newStrategy2 = HODLStrategy()
    # newStrategy3 = MACDStrategy()
    # backtest.addStrategy(newStrategy)
    # backtest.addStrategy(newStrategy2)
    # backtest.addStrategy(newStrategy3)

    newStrategy = RSIDStrategy()
    backtest.addStrategy(newStrategy)
    
    # burada stratejilerde or yapılmalı set olan metod add olamlı alt alta yazılıyorsa kombine ediliyor olmalı 
    # eper add ile ayrı eklendiyse ard arda çalışmalı
 
    backtest.setTradeConditions('buy', {
        'RSIDStrategy' : 'buy',
        # 'HODLStrategy' : 'buy'
    })
    backtest.setTradeConditions('sell', {
        'RSIDStrategy' : 'sell',
        # 'HODLStrategy' : 'sell'
    })
    backtest.setStopPercentage(-1.5)
    tradeSteps = backtest.run()
    
    trade_array = []
    for tradeStep in tradeSteps:
        if(tradeStep['action'] == Strategy.BUY):
            trade_data = {
                    "time": tradeStep['time'] / 1000,
                    "position": 'belowBar',
                    "color": 'green',
                    "shape": 'arrowUp',
                    "text": tradeStep['name'] + ' [' + str(tradeStep['cash']) + ']',
                    "size": 2
                }
            trade_array.append(trade_data)
        elif(tradeStep['action'] == Strategy.SELL):
            trade_data = {
                    "time": tradeStep['time'] / 1000,
                    "position": 'aboveBar',
                    "color": 'red',
                    "shape": 'arrowDown',
                    "text": tradeStep['name'] + ' [' + str(tradeStep['cash']) + ']',
                    "size": 2
                }
            trade_array.append(trade_data)
    
    return Response(json.dumps(trade_array),  mimetype='application/json')

# trade()