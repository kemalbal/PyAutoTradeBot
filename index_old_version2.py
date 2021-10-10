# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, flash, redirect, jsonify
import config
import csv,json
import numpy as np
import talib
from backtest import Backtest
from strategies.Strategy import Strategy
from flask import Response

from strategies.RSIStrategy import RSIStrategy
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
    with open('dataset/binance/2021_jan_15minutes.csv', newline='') as csvfile:
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

@app.route('/trade')
def trade():
    backtest = Backtest()
    backtest.setData('2021_jan_15minutes')

    newStrategy = RSIStrategy()
    newStrategy2 = HODLStrategy()
    newStrategy3 = MACDStrategy()
    backtest.addStrategy(newStrategy)
    backtest.addStrategy(newStrategy2)
    backtest.addStrategy(newStrategy3)
 
    backtest.setTradeConditions('buy', {
        'RSIStrategy' : 'buy',
        # 'HODLStrategy' : 'buy'
    })
    backtest.setTradeConditions('sell', {
        'RSIStrategy' : 'sell',
        # 'HODLStrategy' : 'sell'
    })
    
    backtest.setStopPercentage(5)
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
