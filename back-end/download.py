import requests
import json
import pandas as pd
import datetime as dt

# get 1000 records for 1 requets
# Symbol must be capital
def get_binance_bars(symbol: str, interval: str, startTime: dt.datetime, endTime: dt.datetime) -> pd.core.frame.DataFrame:
    check_startTime = startTime
    symbol = symbol.upper()
    url = 'https://api.binance.com/api/v3/klines'
    startTime = str(int((startTime).timestamp()*1000)) 
    endTime = str(int(endTime.timestamp()*1000))
    limit = '1000'
                         
    req_params = {'symbol': symbol, 'interval': interval, 'startTime': startTime, 'endTime' : endTime, 'limit': limit}
    data = pd.DataFrame(json.loads(requests.get(url, params = req_params).text))
    
    if len(data.columns) == 0:
        return None
    else:                     
        data.drop(data.columns[-1], axis = 1, inplace = True)
        data.columns = ['open_time', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'num_of_trades', 'taker_buy_base', 'taker_buy_quote']
        data.iloc[:,8].astype(int)
        data[data.select_dtypes(['object']).columns] =  data.select_dtypes(['object']).apply(lambda x: x.astype(float))
        data[['open_time', 'close_time']] = data[['open_time', 'close_time']].apply(lambda x: pd.to_datetime(x, unit='ms'))
        data = data[data['open_time'] >= check_startTime]
        # set index by opentime
        data = data.set_index('open_time') 
    return data

#get all records                     
def get_data(symbol: str, interval: str, startTime: dt.datetime, endTime: dt.datetime):
    params_timedelta = dict(days=0, seconds=0, microseconds=0, minutes=0, hours=0, weeks=0, months = 0)
    dict_interval = {'d':'days', 's':'seconds', 'm':'minutes','h':'hours','w': 'weeks', 'M': 'months'}
    params_timedelta[dict_interval[interval[-1]]] = int(interval[0])
                         
    data = get_binance_bars(symbol, interval, startTime, endTime)

    # last_datetime = max(data['open_time']) + pd.DateOffset(**params_timedelta) 
    last_datetime = max(data.index) +  pd.DateOffset(**params_timedelta)  
    df_list = [data] 

    while last_datetime < endTime:
        new_df = get_binance_bars(symbol, interval, last_datetime, endTime)
        if new_df is None:
            break
        else:
            df_list.append(new_df)
            last_datetime = max(new_df.index) + pd.DateOffset(**params_timedelta) 
            # last_datetime = max(data['open_time']) + pd.DateOffset(**params_timedelta) 
    data = pd.concat(df_list)
    # drop last row if kline not finish
    last_datetime = max(data.index) + pd.DateOffset(**params_timedelta) 
    # print(last_datetime)
    # print(dt.datetime.utcnow())
    if(last_datetime > dt.datetime.utcnow()):
        # print('in')
        data = data.drop(data.index[-1])
    return data

if __name__ == '__main__':
    symbol = 'btcusdt'
    interval = '1h'
    startTime = dt.datetime(2021, 1, 15)
    endTime = dt.datetime.now()

    data  = get_data(symbol.upper(), interval, startTime , endTime)
    data.to_csv(f'./klinedata/{symbol}_{interval}.csv', index = True)