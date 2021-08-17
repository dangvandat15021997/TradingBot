import re
from signals.Signal import signal
from fastapi import FastAPI, Request, Form, params
from starlette.responses import RedirectResponse
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from populate_db.update_coin_price import update_coin_price
from fastapi.middleware.cors import CORSMiddleware
# from tortoise.contrib.fastapi import register_tortoise
import sqlite3 as sql
import config
import signals as sn
import json

from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import json_item

# Read row as dictionary in sql3
def dict_factory(cursor, row):
    dictionary = {}
    for idx, col in enumerate(cursor.description):
        dictionary[col[0]] = row[idx]
    return dictionary

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# update coin_price
update_coin_price()

origins = [
    'http://localhost:3000'
]
# add middleware and specify cors
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# register_tortoise(
#     app,
#     db_url='sqlite://database.sqlite3',
#     modules={'models': ['models']},
#     generate_schemas = True,
#     add_exception_handlers = True
# )


@app.get("/")
async def index(request: Request):
 
    #create db conn
    conn = sql.connect(config.DB_URL)
    conn.row_factory = sql.Row
    cursor = conn.cursor()
    symbols = []
    
    params_dict = request.query_params._dict
    if 'signal_filter' not in params_dict:
        conn = sql.connect(config.DB_URL)
        conn.row_factory = sql.Row
        cursor = conn.cursor()

        select_query = '''SELECT DISTINCT symbol from coin_pair '''
        cursor.execute(select_query)
        rows = cursor.fetchall()
        for row in rows:
            symbols.append(row)
    elif params_dict['signal_filter'] == 'All':
        conn = sql.connect(config.DB_URL)
        conn.row_factory = sql.Row
        cursor = conn.cursor()

        select_query = '''SELECT DISTINCT symbol from coin_pair '''
        cursor.execute(select_query)
        rows = cursor.fetchall()
        for row in rows:
            symbols.append(row)
  
    else:
        signal_name = params_dict['signal_filter']
        signal = getattr(sn, signal_name)
        select_query = '''SELECT DISTINCT symbol from coin_pair '''
        cursor.execute(select_query)
        rows = cursor.fetchall()
        for row in rows:
            is_over = signal.signal(row['symbol'])
            if is_over:
                symbols.append(row)
    
    select_query = '''SELECT DISTINCT name from signal '''
    cursor.execute(select_query)
    rows = cursor.fetchall()
    signal_list = []
    for row in rows:
        signal_list.append(row['name'])
        
    
    conn.commit()
    conn.close()
    
    return templates.TemplateResponse("index.html", {"request": request, "symbols": symbols, "signal_list": signal_list})


@app.get("/coin/")
async def coin(request: Request):
    symbol = request.query_params['symbol']
    #create db conn
    conn = sql.connect(config.DB_URL)
    conn.row_factory = sql.Row
    cursor = conn.cursor()


    #create list exist symbol
    # get symbol interval
    select_query = '''SELECT open_time, open, high, low, close, close_time, volume 
                      from coin_pair a inner join coin_price b on (a.id = b.id_coin_pair)
                      where symbol = ? '''
    cursor.execute(select_query, (symbol,))
    rows = cursor.fetchall()
    templates = Jinja2Templates(directory="templates")
    

    # # select strategy
    # select_query = '''SELECT name from strategy'''
    # cursor.execute(select_query)
    # strategy = cursor.fetchall()

    conn.commit()
    conn.close()

    templates = Jinja2Templates(directory="templates")

    return templates.TemplateResponse("coin_detail.html", {"request": request, "rows": rows, "symbol":symbol}) 

@app.post("/apply_strategy")
async def apply_strategy(strategy_id: int = Form(...), id_symbol: int = Form(...)):
    
    #create db conn
    conn = sql.connect('app.db')
    conn.row_factory = sql.Row
    cursor = conn.cursor()
    templates = Jinja2Templates(directory="templates")

    #create list exist symbol
    # get symbol interval
    cursor.execute('''Select distinct symbol from coin_pair where id = ?''', (id_symbol,))
    result = cursor.fetchone()
    symbol = result['symbol']
    
    select_query = '''INSERT INTO coin_strategy(symbol, id_strategy) VALUES(?,?)'''
    cursor.execute(select_query, (symbol,strategy_id))
    

    conn.commit()
    conn.close()


    return RedirectResponse(url = f'/strategy/?strategy_id={strategy_id}', status_code = 303)  

"""
Back-End React start from here!
"""

#indicator api

@app.get("/indicator/{id_signal}")
async def get_indicators(id_signal: int):
    if id_signal == 0:
        return json.dumps([])
    #create db conn
    conn = sql.connect('app.db')
    conn.row_factory = dict_factory
    cursor = conn.cursor()

    

    select_query = """SELECT DISTINCT id_signal, id_indicator, interval
                    FROM indicator 
                    WHERE id_signal = ? """
                      
    cursor.execute(select_query, (id_signal, ))
    rows = cursor.fetchall()
    
    result = list()

    for row in rows:
        id_signal = row['id_signal']
        id_indicator = row['id_indicator']
        interval = row['interval']
        
        select_query = """WITH RECURSIVE 
                      indicator_distinct AS (
                      SELECT DISTINCT id_indicator, id_signal, interval
                      FROM indicator
                      )
                      SELECT params_name, value
                      FROM indicator_distinct NATURAL JOIN indicator
                      WHERE id_signal = ? and id_indicator = ? and interval = ?"""
        
        cursor.execute(select_query, (id_signal, id_indicator, interval,))
        result_rows = cursor.fetchall()
        temp_dict = dict()
        for params in result_rows:
            temp_dict[params['params_name']] = params['value'] 
        temp_dict["id_indicator"] = id_indicator     
        result.append(temp_dict)

    
    return json.dumps(result)
        





#Signal api
@app.get("/signal")
async def get_all_signal(request: Request):
    #create db conn
    conn = sql.connect('app.db')
    conn.row_factory = dict_factory
    cursor = conn.cursor()

    

    #create list exist symbol
    # get symbol interval
    cursor.execute('''Select * from signal ''')
    rows = cursor.fetchall()

    result = []
    # add result to lis of dict
    for row in rows:
        result.append(row)

    

    conn.commit()
    conn.close()


    return json.dumps(result)

#get symbol by signal
@app.get("/signal/{id_signal}")
async def get_signal_filter(request: Request, id_signal: int):
    #update coin_price
    # update_coin_price()
    #create db conn
    conn = sql.connect(config.DB_URL)
    conn.row_factory = dict_factory
    cursor = conn.cursor()
    symbols = []

    #get signal_name
    select_query = '''SELECT * from signal where id = ? '''
    cursor.execute(select_query, (id_signal, ))
    row = cursor.fetchone()


    if row == None:
        print('Im in!')
        select_query = '''SELECT DISTINCT symbol from coin_pair '''
        cursor.execute(select_query)
        rows = cursor.fetchall()
        for row in rows:
            symbols.append(row)
  
    else:
        signal_name = row['name']
        signal = getattr(sn, signal_name)
        select_query = '''SELECT DISTINCT symbol from coin_pair '''
        cursor.execute(select_query)
        rows = cursor.fetchall()
        for row in rows:
            is_over = signal.signal(row['symbol'])
            if is_over:
                symbols.append(row)
    
        
    conn.commit()
    conn.close()
    
    return json.dumps(symbols)

# Strategy
@app.get("/strategy")
async def get_all_strategy(request: Request):
    #connect to DB
    conn = sql.connect(config.DB_URL)
    conn.row_factory = dict_factory
    cursor = conn.cursor()

    selected_query = """ Select distinct name from strategy"""
    cursor.execute(selected_query)

    rows = cursor.fetchall()
    result = []

    for row in rows:
        result.append(row)

    return json.dumps(result)


# Test 
import sys
sys.path.append("./backtrader")
from backtrader_plotting import Bokeh
from backtrader_plotting.schemes import Tradimo
from bokeh.io import output_file, show, save
from bokeh.plotting import figure
from bokeh.embed import components
from backtrader_plotting import Bokeh
import backtrader as bt
import datetime
from datafeed import create_coin_price_datafeed
from bokeh.embed import file_html, json_item

@app.get("/test")
async def get_test(request: Request):

    class TestStrategy(bt.Strategy):
        params = (
            ('buydate', 21),
            ('holdtime', 6),
        )

        def next(self):
            if len(self.data) == self.p.buydate:
                self.buy(self.datas[0], size=None)

            if len(self.data) == self.p.buydate + self.p.holdtime:
                self.sell(self.datas[0], size=None)



    cerebro = bt.Cerebro()

    cerebro.addstrategy(TestStrategy, buydate=3)

    data = create_coin_price_datafeed(symbol = 'BTCUSDT', interval = '1d')
    cerebro.adddata(data)

    cerebro.run()

    b = Bokeh(style='bar', tabs='multi', scheme=Tradimo(),
    toolbar_location='right', show = False, output_mode = 'save')
    test = cerebro.plot(b)
    tabs = test[0][0].model

    result = json.dumps(json_item(tabs, "myplot"))
    
    return result

@app.get("/test_strategy")
async def get_test_strategy(request: Request):

    class SmaCross(bt.Strategy):
    # list of parameters which are configurable for the strategy
        params = dict(
            pfast=50,  # period for the fast moving average
            pslow=200   # period for the slow moving average
        )

        def __init__(self):
            self.order = None
            sma1 = bt.ind.EMA(period=self.p.pfast)  # fast moving average
            sma2 = bt.ind.EMA(period=self.p.pslow)  # slow moving average
            self.crossover = bt.ind.CrossOver(sma1, sma2)  # crossover signal
        
        def log(self, txt, dt=None):
            ''' Logging function fot this strategy'''
            dt = dt or self.datas[0].datetime.date(0)
            print('%s, %s' % (dt.isoformat(), txt))
            
        def notify_order(self, order):
            if order.status in [order.Submitted, order.Accepted]:
                # Buy/Sell order submitted/accepted to/by broker - Nothing to do
                return

            # Check if an order has been completed
            # Attention: broker could reject order if not enough cash
            if order.status in [order.Completed]:
                if order.isbuy():
                    self.log(
                        'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                        (order.executed.price,
                        order.executed.value,
                        order.executed.comm))

                    self.buyprice = order.executed.price
                    self.buycomm = order.executed.comm
                else:  # Sell
                    self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                            (order.executed.price,
                            order.executed.value,
                            order.executed.comm))

            elif order.status in [order.Canceled, order.Margin, order.Rejected]:
                self.log('Order Canceled/Margin/Rejected')

            # Write down: no pending order
            self.order = None

        def notify_trade(self, trade):
            if not trade.isclosed:
                return

            self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                    (trade.pnl, trade.pnlcomm))

        def next(self):
            if not self.position:  # not in the market
                if self.crossover > 0:  # if fast crosses slow to the upside
                    limit_price = self.datas[0].close
                    size = float()
                    self.buy()  # enter long

            elif self.crossover < 0:  # in the market & cross to the downside
                self.close()  # close long position



    cerebro = bt.Cerebro()

    cerebro.addstrategy(SmaCross)

    data = create_coin_price_datafeed(symbol = 'BTCUSDT', interval = '1d')
    cerebro.adddata(data)

    cerebro.run()

    b = Bokeh(style='bar', tabs='multi', scheme=Tradimo(),
    toolbar_location='right', show = False, output_mode = 'save')
    test = cerebro.plot(b)
    tabs = test[0][0].model

    result = json.dumps(json_item(tabs, "myplot"))
    
    return result
