from strategies.Strategy import Strategy
import talib, numpy as np

class HODLStrategy(Strategy):
    def next(self, lastData):
        if(lastData):
            return self.SELL
        close = self.getData('close')
        if(len(close) == 1):
            return self.BUY  
        return False
