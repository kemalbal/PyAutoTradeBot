from strategies.Strategy import Strategy
import talib
import numpy as np

class RSIDStrategy(Strategy):
    position_price = 0

    def next(self, lastData):
        close = self.getData('close')
        open = self.getData('open')
        rsi = talib.RSI(close, timeperiod=14)
  
        # if(not np.isnan(rsi[-1])):
        #     self.info = rsi[-1]
        #     rsi_value = float(rsi[-1])
        #     if(rsi_value > 70):
        #         return self.SELL

        #     if(rsi_value < 30):
        #         return self.BUY
        if(self.position_price  > 0):
            if(self.position_price * 1.015 <= close[-1]):
                self.position_price = 0
                return self.SELL 

        return self.detect_divergence(open, close, rsi)

    def detect_divergence(self, open, close, rsi):
        #green bar
        if(open[-1] < close[-1]):
            if(not np.isnan(rsi[-1])):
                current_rsi = -1
                current_close = -1
                before_current_min_close = -1
                for i in range(len(rsi) - 1, len(rsi) - 10, -1):
                    if(current_rsi == -1 and current_close == -1):
                        #red bar
                        if(open[i] > close[i]):
                            current_rsi = rsi[i]
                            current_close = close[i]
                    elif(close[i] > current_close):
                        if(rsi[i] < current_rsi):
                            # bull
                            self.info = '-'.join(['Sira:' + str(len(rsi) - i) + 'AAA', str(rsi[i]), str(current_rsi)])
                            self.position_price = close[-1]
                            return self.BUY
        return False