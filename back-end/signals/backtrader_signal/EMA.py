import backtrader as bt

class EMA(bt.Strategy):
    params = dict(
        period = 200, 
        interval = '1d',
        minimumPeriod = 201
    )
    
    def __init__(self):
    #     self.p.minimumPeriod = self.p.period +1
        self.sma = bt.ind.EMA(self.datas[0].close, period=self.p.period)  # fast moving average
        self.signal = bt.If(bt.And(self.datas[0].close > self.sma, self.datas[0].close > self.sma), 1, 0)

    def next(self):
        pass