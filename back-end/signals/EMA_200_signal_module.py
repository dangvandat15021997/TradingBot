# System library import
from __future__ import absolute_import
import sys
sys.path.append("../")
import sqlite3 as sql
import numpy as np
# print(f"Name : {__name__}")


# Third party library import 
import backtrader as bt
import pandas_ta as ta  


# Self-defined library import
from backtrader_custom.datafeed import createCoinPriceDatafeed, fetchAsPandas
from backtrader_custom.backtrader_signals import EMA
import config

if __name__ == "__main__":
    from signal_module import signal
else:
    from .signal_module import signal   



class EMA_200_signal(signal):
    
    def __init__(self, name):
        self.bt_strategy = EMA
        self.interval = self.bt_strategy.params.interval
        print(self.interval)
        self.name = name
        self.indicators = [
            { "id": "EMA",  
            "interval" : self.interval,
             "inputs" :
             {
                "length" : 200,
                "source" : "close",
                "offset" : 0
             } 
            }
        ]
        
        
    def backtest(self, symbol):
        interval =  self.bt_strategy.params.interval
        # Create a data feed
        data_feed = createCoinPriceDatafeed(symbol, interval)
        cerebro = bt.Cerebro() 
        cerebro.adddata(data_feed)  # Add the data feed
        cerebro.addstrategy(self.bt_strategy)  # Add the trading strategy
        self.result = cerebro.run()  # run it all

        cerebro.plot()

        
    
    def signal(self, symbol):
        #create db conn
        conn = sql.connect(config.DB_URL)
        conn.row_factory = sql.Row
        cursor = conn.cursor()


        #create list exist symbol
        select_query = '''SELECT close, open
                          FROM coin_pair a INNER JOIN coin_price b on (a.id = b.id_coin_pair)
                          WHERE a.symbol = ? and a.interval = ?
                          ORDER BY b.close_time ASC'''
        
        pandas_result = fetchAsPandas(select_query, symbol, self.interval)
        latest_close = pandas_result["close"].iloc[-1]
        latest_open = pandas_result["open"].iloc[-1]

        ema_200 = ta.ema(pandas_result["close"], length=200)
        is_over = None

        print(latest_close)
        print(latest_open)
        print(ema_200)

        if latest_close >= ema_200.iloc[-1] and latest_open >= ema_200.iloc[-1]:
            is_over = True
        else:
            is_over = False

        return is_over


if __name__ == '__main__':
    test = EMA_200_signal(name = "abc")
    a = test.signal('BTCUSDT')

        
        
        
  