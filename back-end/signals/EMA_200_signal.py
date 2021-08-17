from __future__ import absolute_import
import sys
sys.path.append('C:\\Users\\X_X\\Desktop\\TraddingBot\\back-end\\signals')
sys.path.append('C:\\Users\\X_X\\Desktop\\TraddingBot\\back-end\\signals\\backtrader_signal')
sys.path.append('C:\\Users\\X_X\\Desktop\\TraddingBot\\back-end\\backtrader')
sys.path.append('C:\\Users\\X_X\\Desktop\\TraddingBot\\back-end')

from Signal import signal
from datafeed import create_coin_price_datafeed
from EMA import EMA
import config
import backtrader as bt
import sqlite3 as sql
import numpy as np
import talib



class EMA_200_signal(signal):
    
    def __init__(self, name):
        self.bt_strategy = EMA
        self.interval = self.bt_strategy.params.interval
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
        data_feed = create_coin_price_datafeed(symbol, interval)
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
                          ORDER BY b.close_time DESC'''
        cursor.execute(select_query, (symbol,self.interval))
        closes = []
        rows = cursor.fetchall()
        latest_open = None
        is_assign = False
        for row in rows:
            if not is_assign:
                latest_open = row['open']
                is_assign = True
            closes.append(row['close'])

        latest_close = closes[0]

        conn.commit()
        conn.close()


        ema_200 = talib.EMA(np.array(closes)[::-1], timeperiod=200)
        is_over = None

#         print(ema_200)

        if latest_close >= ema_200[-1] and latest_open >= ema_200[-1]:
            is_over = True
        else:
            is_over = False

        return is_over


if __name__ == '__main__':
    test = EMA_200_signal(name = "abc")
    test.signal('BTCUSDT')
        
        
  