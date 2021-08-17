from __future__ import absolute_import
import sys
sys.path.append('../')
from download import get_data
from binance.client import Client
import datetime as dt
import config
import sqlite3 as sql
import pandas as pd
import numpy as np
from update_coin_price import update_coin_price


def update_coin_pair():
    # creat client
    client = Client(config.API_KEY, config.API_SECRET, tld='us')

    # create db conn
    conn = sql.connect(config.DB_URL)
    conn.row_factory = sql.Row
    cursor = conn.cursor()

    # create list exist symbol
    select_query = '''SELECT DISTINCT symbol FROM coin_pair'''
    cursor.execute(select_query)
    rows = cursor.fetchall()
    symbols_existed = [row['symbol'] for row in rows]

    # insert query
    insert_coin_pair = '''INSERT INTO coin_pair(symbol, interval) VALUES(?,?)'''
    # print(symbols_existed)

    # get exchange info
    exchange_info = client.get_exchange_info()

    # insert to db
    for s in exchange_info['symbols']:
        try:
            if (s['symbol'][-4:].lower() == 'usdt') and (s['status'] == "TRADING") and (s['symbol'] not in symbols_existed):
                for interval in config.KLINE_INTERVAL_LIST:
                    conn.execute(insert_coin_pair, (s['symbol'], interval))
                    print(s['symbol'] + interval)
        except Exception as e:
            print('error')

    print('update coin_pair is done!')
    conn.commit()
    conn.close()


if __name__ == '__main__':
    update_coin_pair()
    update_coin_price()
