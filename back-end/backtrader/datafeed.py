import sys
sys.path.append("../")
sys.path.append("C:\\Users\\X_X\\Desktop\\TraddingBot\\back_end\\")

import backtrader as bt
import sqlite3 as sql
import config
import pandas as pd

def fetchAsPandas(query, *params):
    list_params = []
    for param in params:
        list_params.append(param)
    
    conn = sql.connect(config.DB_URL, detect_types=sql.PARSE_DECLTYPES)
    cur = conn.cursor()
    query_result = cur.execute(query, list_params)
    cols = [column[0] for column in query_result.description]
    results= pd.DataFrame.from_records(data = query_result.fetchall(), columns = cols)
    conn.close()
    
    return results

def fetch_coin_price_as_pandas(symbol, interval):
    symbol = symbol.upper()
    select_query = '''SELECT open_time as datetime, open, high, low, close, volume 
                   from coin_pair a inner join coin_price b on (a.id = b.id_coin_pair)
                   where symbol = ? and interval = ? '''
    result = fetchAsPandas(select_query, symbol, interval)
    result = result.set_index('datetime')
    
    return result

def create_coin_price_datafeed(symbol, interval, **kwargs):
    data = fetch_coin_price_as_pandas(symbol, interval)
    name = symbol.upper()+ '_' + interval.upper()
    
    return bt.feeds.PandasData(dataname = data, name = name, **kwargs)

def get_all_datafeed(interval, **kwargs):
    
    conn = sql.connect(config.DB_URL)
    conn.row_factory = sql.Row
    cur = conn.cursor()
    
    select_query = "SELECT DISTINCT symbol FROM coin_pair where interval = ?"
    rows = cur.execute(select_query, (interval, ))
    result_list = []
    
    
    for row in rows:
        new_dataFeed = create_coin_price_datafeed(row['symbol'], interval, **kwargs)
        result_list.append(new_dataFeed)
    
    conn.close()
    
    return result_list