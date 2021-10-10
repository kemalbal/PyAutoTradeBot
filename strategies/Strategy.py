import numpy as np 

class Strategy():
    BUY = 1
    SELL = 2

    data = []
    info = ''
    
    def __init__(self):
        self.name = self.__class__.__name__

    def changeName(self, name):
        self.name = name 

    def addData(self, time, open, high, low, close, volume, close_time):
        self.data.append({
            'time' : time,
            'open' : open,
            'high' : high,
            'low' : low,
            'close' : close,
            'volume' : volume,
            'close_time' : close_time,
        })
    
    def getData(self, key = 'all'):
        if(key == 'all'):
            return self.data
        return np.array(list(map(lambda x : x[key], self.data)))