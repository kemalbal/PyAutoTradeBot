from strategies.Strategy import Strategy
import talib, numpy as np

class RSIStrategy(Strategy):
    def next(self, lastData):
        close = self.getData('close')
        rsi = talib.RSI(close, timeperiod=14)
        if(not np.isnan(rsi[-1])):
            self.info = rsi[-1]
            if(rsi[-1] > 70):
                return self.SELL
            
            if(rsi[-1] < 30):
                return self.BUY
            
        return False