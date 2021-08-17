import websocket as ws
import numpy as np
import json, pprint, talib
import config
import datetime as dt
from binance.client import Client
from binance.enums import *
from download import get_data
from strategy import RSI_strategy
from datastream import read_csv, read_stream_row

# constant
INTERVAl = '1h'
SYMBOL = 'ethusdt'
SOCKET = f"wss://stream.binance.com:9443/ws/{SYMBOL}@kline_{INTERVAl}"
STARTTIME = dt.datetime(2019, 8, 15)
ENDTIME = dt.datetime.now()
IN_POSITION = False

data  = get_data(SYMBOL.upper(), INTERVAl, STARTTIME , ENDTIME)
data.to_csv(f'klinedata/{SYMBOL}_{INTERVAl}.csv', index = True)


#client
client = Client(config.API_KEY, config.API_SECRET, tld='vi')

def order(side, quantity, symbol,order_type=ORDER_TYPE_MARKET):
    try:
        print("sending order")
        order = client.create_order(symbol=symbol, side=side, type=order_type, quantity=quantity)
        print(order)
    except Exception as e:
        print("an exception occured - {}".format(e))
        return False

    return True

    
def on_open(ws):
    print('opened connection')

def on_close(ws):
    print('closed connection')

def on_message(ws, message):
    global closes, in_position
    
    print('received message')
    json_message = json.loads(message)

    candle = json_message['k']

    is_candle_closed = candle['x']
    close = candle['c']

    if is_candle_closed:
        print("candle closed at {}".format(close))
        csv_file = pd.read_csv()
        closes.append(float(close))
        print("closes")
        print(closes)

        if len(closes) > RSI_PERIOD:
            np_closes = np.array(closes)
            rsi = talib.RSI(np_closes, RSI_PERIOD)
            print("all rsis calculated so far")
            print(rsi)
            last_rsi = rsi[-1]
            print("the current rsi is {}".format(last_rsi))

            if last_rsi > RSI_OVERBOUGHT:
                if in_position:
                    print("Overbought! Sell! Sell! Sell!")
                    # put binance sell logic here
                    order_succeeded = order(SIDE_SELL, TRADE_QUANTITY, TRADE_SYMBOL)
                    if order_succeeded:
                        in_position = False
                else:
                    print("It is overbought, but we don't own any. Nothing to do.")
            
            if last_rsi < RSI_OVERSOLD:
                if in_position:
                    print("It is oversold, but you already own it, nothing to do.")
                else:
                    print("Oversold! Buy! Buy! Buy!")
                    # put binance buy order logic here
                    order_succeeded = order(SIDE_BUY, TRADE_QUANTITY, TRADE_SYMBOL)
                    if order_succeeded:
                        in_position = True

                
ws_app = ws.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_message=on_message)
ws_app.run_forever()