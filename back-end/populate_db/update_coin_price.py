import sys
sys.path.append('../')
import numpy as np
import pandas as pd
import sqlite3 as sql
import config
import datetime as dt
from binance.client import Client
from download import get_data


# insert one symbol interval
def update_interval_coin_price(symbol, interval):
    # connect db
    conn = sql.connect(
        config.DB_URL, detect_types=sql.PARSE_DECLTYPES | sql.PARSE_COLNAMES)
    conn.row_factory = sql.Row
    cursor = conn.cursor()
    
    # set param for pd.DateOffset
    params_timedelta = dict(
        days=0, seconds=0, microseconds=0, minutes=0, hours=0, weeks=0, months=0)
    dict_interval = {'d': 'days', 's': 'seconds',
                     'm': 'minutes', 'h': 'hours', 'w': 'weeks', 'M': 'months'}
    params_timedelta[dict_interval[interval[-1]]
                     ] = int(interval[0])
   
    # get the lates open time
    latest_opentime_query = '''SELECT * 
                            FROM coin_pair a INNER JOIN coin_price b ON (a.id = b.id_coin_pair)
                            WHERE a.symbol = ? and a.interval = ?
                            ORDER BY open_time DESC LIMIT 1;'''
    cursor.execute(latest_opentime_query, (symbol, interval))
    rows = cursor.fetchone()
    
    conn.close()

    # check is symbol and interval is exist in coin_price
    # if not download from 1/1/2017
    if rows is None:
        start_time = dt.datetime(2017, 1, 1)
        print(
            f'start time: {start_time}, interval: {interval}, symbol: {symbol}')
        new_data = get_data(
            symbol, interval, start_time, dt.datetime.now())
        new_data.rename(
            columns={new_data.columns[-1]: new_data.columns[-1].strip()}, inplace=True)
        new_data = new_data.reset_index()
        insert_coin_price(symbol, interval, new_data)
    else:
        # start time = last open time + interval
        start_time = (
            rows['open_time'] + pd.DateOffset(**params_timedelta)).to_pydatetime()
        close_time = start_time + pd.DateOffset(**params_timedelta)
        if (close_time > dt.datetime.utcnow()):
            print(
                f'interval: {interval}, symbol: {symbol} is up to date!')
        elif (start_time < dt.datetime.now()):
            print(
                f'start time: {start_time}, interval: {interval}, symbol: {symbol}')
            new_data = get_data(
                symbol, interval, start_time, dt.datetime.now())
            new_data.rename(
                columns={new_data.columns[-1]: new_data.columns[-1].strip()}, inplace=True)
            new_data = new_data.reset_index()
            insert_coin_price(symbol, interval, new_data)
        else:
            print(
                f'interval: {interval}, symbol: {symbol} is up to date!')

def update_coin_price():
    # create db conn
    conn = sql.connect(
        config.DB_URL, detect_types=sql.PARSE_DECLTYPES | sql.PARSE_COLNAMES)
    conn.row_factory = sql.Row
    cursor = conn.cursor()

    # create list exist symbol
    select_query = '''SELECT DISTINCT symbol FROM coin_pair;'''
    cursor.execute(select_query)
    rows = cursor.fetchall()
    symbols_existed = [row['symbol'] for row in rows]

    if symbols_existed:
        for symbol in symbols_existed:
            for interval in config.KLINE_INTERVAL_LIST:
                update_interval_coin_price(symbol, interval)
    else:
        pass
    print('coin_price is up to date!')

    conn.commit()
    conn.close()


# insert data from dataframe
def insert_coin_price(symbol, interval, new_data):
    try:
        conn = sql.connect(
            config.DB_URL, detect_types=sql.PARSE_DECLTYPES | sql.PARSE_COLNAMES)
        conn.row_factory = sql.Row
        cursor = conn.cursor()
        # get id_coin pair from coin_pair table
        id_coin_pair_query = '''SELECT DISTINCT id 
                                FROM coin_pair a
                                WHERE a.symbol = ? and a.interval = ? '''
        cursor.execute(id_coin_pair_query, (symbol, interval))
        id_coin_pair_rows = cursor.fetchone()
        # if not exist insert new one to table
        if id_coin_pair_rows is None:
            new_query = '''INSERT INTO coin_pair(symbol, interval) VALUES(?,?)'''
            cursor.execute(new_query, (symbol, interval))
            cursor.execute(id_coin_pair_query, (symbol, interval))
            id_coin_pair_rows = cursor.fetchone()

        # insert data
        id_coin_pair = id_coin_pair_rows['id']
#         print(id_coin_pair)
        new_col = np.ones(len(new_data))
        new_col = np.where(new_col == 1, id_coin_pair, new_col)
        new_data['id_coin_pair'] = pd.Series(new_col)
        new_data.to_sql(name='coin_price', con=conn,
                        if_exists='append', index=False)
    except Exception as e:
        print(e)
        print(id_coin_pair)
    conn.commit()
    conn.close()
