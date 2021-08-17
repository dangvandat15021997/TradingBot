import numpy as np
import talib
import pandas as np


def RSI_strategy(data, in_positon):
    RSI_PERIOD = 14
    RSI_OVERBOUGHT = 70
    RSI_OVERSOLD = 30
    MAKE_BUY_ORDER = False
    MAKE_SELL_ORDER = False

    closes = data['Close']

    if len(closes) > RSI_PERIOD:
        np_closes = np.array(closes)
        rsi = talib.RSI(np_closes, RSI_PERIOD)
        print(rsi)
        last_rsi = rsi[-1]
        print("the current rsi is {}".format(last_rsi))

        if last_rsi > RSI_OVERBOUGHT:
            if in_position:
                print("Sell RSI signal!")
                # put binance sell logic here
                MAKE_SELL_ORDER = True
            else:
                print("It is overbought, but we don't own any. Nothing to do.")
        
        if last_rsi < RSI_OVERSOLD:
            if in_position:
                print("It is oversold, but you already own it, nothing to do.")
            else:
                print("Oversold! Buy! Buy! Buy!")
                MAKE_BUY_ORDER = True

    return MAKE_BUY_ORDER, MAKE_SELL_ORDER

    




    



                
