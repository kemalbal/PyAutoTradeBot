#%%
import numpy as np 
import os 
from strategies.Strategy import Strategy

#%%
class Backtest():
    strategies = []
    inPosition = False 
    positionCoinPrice = 0
    coinAmount = 0
    cash = 1000
    tradeBuyCondions = {}
    tradeSellCondions = {}
    stopPercentage = 0

    def __init__(self, baseDataPath = 'dataset'):
        self.baseDataPath = baseDataPath

    def setData(self, dataFile):
        type = 'binance'
        self.data = np.genfromtxt(os.path.sep.join([self.baseDataPath, type, dataFile]) + '.csv', delimiter=',')

    def setCash(self, cash):
        self.cash = cash

    def addStrategy(self, strategy):
        self.strategies.append(strategy)

    def buy(self, coinPrice):
        self.inPosition = True
        self.coinAmount = self.cash / coinPrice
        self.cash = 0
        self.positionCoinPrice = coinPrice
    
    def sell(self, coinPrice):
        self.inPosition = False
        self.cash = self.coinAmount * coinPrice
        self.coinAmount = 0
        self.positionCoinPrice = 0
        
    def getSignals(self):
        signals = []
        for data in self.data:
            timeAdded = True
            for strategy in self.strategies:
                time = data[0]
                open = data[1]
                high = data[2]
                low = data[3]
                close = data[4]
                volume = data[5]
                close_time = data[6]
                if(timeAdded):
                    strategy.addData(time, open, high, low, close, volume, close_time)
                    timeAdded = False
                signal = strategy.next(self.data[-1][0] == time)
                if(signal != False):
                    signals.append({
                        'name' : strategy.name,
                        'time' : time,
                        'price' : close,
                        'action' : signal,
                        'info' : strategy.info
                    })
        return signals

    # stopta fitillere de bakılmalı
    def setStopPercentage(self, percentage):
        self.stopPercentage = percentage

    def setTradeConditions(self, action, condition):
        if(action == 'buy'):
            self.tradeBuyCondions = condition
        elif(action == 'sell'):
            self.tradeSellCondions = condition

    # şu andaki durumda indikatörler farklı yerlerde al verse bile al vermeye devam ederken koşul sağlanabilir sata dönene kadar 
    def run(self):
        signals = self.getSignals()
        stepSignals = {}
        tradeSteps = []
        

        for data in self.data:
            time = data[0]
            open = data[1]
            high = data[2]
            low = data[3]
            close = data[4]
            volume = data[5]
            close_time = data[6]
            messages = []
            for signal in [signal for signal in signals if signal['time'] == time]:
                if(signal['info'] != ''):
                    messages.append(str(signal['info']))
                stepSignals[signal['name']] = 'buy' if signal['action'] == Strategy.BUY else 'sell'

            buy = True
            sell = True
            for buyCondition in self.tradeBuyCondions:
                if(buyCondition not in stepSignals or stepSignals[buyCondition] != self.tradeBuyCondions[buyCondition]):
                    buy = False
                    break
            for sellCondition in self.tradeSellCondions:
                if(sellCondition not in stepSignals or stepSignals[sellCondition] != self.tradeSellCondions[sellCondition]):
                    sell = False
                    break
            
            if(buy):
                if(not self.inPosition):
                    tradeSteps.append({
                        'name' : str(len(tradeSteps)) + ' BUY ' + "-".join(messages),
                        'time' : time,
                        'price' : close,
                        'cash' : self.cash,
                        'action' : Strategy.BUY
                    })
                    self.buy(close)
            elif(sell):
                if(self.inPosition):
                    # Burada stop varsa stopa kadar bekletilebilir eğer zarardaysa 
                    self.sell(close)
                    tradeSteps.append({
                        'name' : str(len(tradeSteps)) + ' SELL ' + "-".join(messages),
                        'time' : time,
                        'price' : close,
                        'cash' : self.cash,
                        'action' : Strategy.SELL
                    })
                    
            if(self.inPosition):
                if(self.stopPercentage > 0):
                    if(self.positionCoinPrice * (1 - self.stopPercentage / 100) >= low):
                        self.sell(close)
                        tradeSteps.append({
                            'name' : str(len(tradeSteps)) + ' STOP ' + "-".join(messages),
                            'time' : time,
                            'price' : close,
                            'cash' : self.cash,
                            'action' : Strategy.SELL
                        })
                        
        return tradeSteps

    
#%%
# backtest = Backtest()
# # %%

# class RSIStrategy(Strategy):
#     def next(self, time, price):
#         return False

# newStrategy = RSIStrategy()

# backtest.setData('2021_jan_15minutes')

# backtest.addStrategy(newStrategy)

# backtest.run()
# %%
