import pandas as pd
import numpy as np
import datetime as dt

#return dataframe with opentime index
def read_csv(SYMBOL, INTERVAl):
    data = pd.read_csv(f'klinedata/{SYMBOL}_{INTERVAl}.csv', index_col = 0)
    data.index = pd.to_datetime(data.index)
    data['close_time'] = pd.to_datetime(data['close_time'])
    return data

#return dataframe with opentime index
def read_stream_row(kline_data):
    columns_dict = {'t':'open_time', 'o':'Open', 'h':'high', 'l':'low', 'c':'Close', 'v':'volume', 'T':'close_time', 'q':'quote_asset_volume', 'n':'num_of_trades', 'V':'taker_buy_base', 'Q':'taker_buy_quote '}
    value_dict = dict()
    for key in kline_data:
        if key in columns_dict.keys():
            col_name = columns_dict[key]
            value_dict[col_name] = [kline_data[key]]
    new_row = pd.DataFrame(value_dict)
    new_row[new_row.select_dtypes(['object']).columns] =  new_row.select_dtypes(['object']).apply(lambda x: x.astype(float))
    new_row[['open_time', 'close_time']] = new_row[['open_time', 'close_time']].apply(lambda x: pd.to_datetime(x, unit='ms'))
    new_row = new_row.set_index('open_time') 
    return new_row