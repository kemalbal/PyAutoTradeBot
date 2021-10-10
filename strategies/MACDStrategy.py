from strategies.Strategy import Strategy
import talib, numpy as np

class MACDStrategy(Strategy):
    def next(self, lastData):
        close = self.getData('close')
        time = self.getData('time')
        macd, macdsignal, macdhist = talib.MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)
        # print(time[-1], close[-1], macd[-1], macdsignal[-1], macdhist[-1])
        # if(not np.isnan(rsi[-1])):
        #     if(rsi[-1] > 70):
        #         return self.SELL
            
        #     if(rsi[-1] < 30):
        #         return self.BUY
            
        return False