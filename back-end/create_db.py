import sqlite3 as sql
import config


def create_db():
    conn = sql.connect(config.DB_URL)

    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS coin_pair (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        symbol TEXT NOT NULL ,
        interval TEXT NOT NULL,
        UNIQUE(symbol,interval)
    ); """)

    cursor.execute("""CREATE TABLE IF NOT EXISTS coin_price ( 
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_coin_pair INTEGER NOT NULL,
        open_time TIMESTAMP  NOT NULL,
        open NOT NULL,
        high NOT NULL,
        low NOT NULL,
        close NOT NULL,
        volume NOT NULL,
        close_time TIMESTAMP  NULL,
        quote_asset_volume NOT NULL,
        num_of_trades NOT NULL,
        taker_buy_base NOT NULL,
        taker_buy_quote NOT NULL, 
        UNIQUE(id_coin_pair, open_time),
        FOREIGN KEY (id_coin_pair) REFERENCES coin_pair(id) ON DELETE CASCADE
    );""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS signal ( 
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name Text NOT NULL,
        UNIQUE(name)
    );""")


    cursor.execute("""CREATE TABLE IF NOT EXISTS indicator ( 
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_indicator INTEGER NOT NULL,
        id_signal INTEGER NOT NULL,
        interval TEXT NOT NULL, 
        params_name TEXT NOT NULL,
        value REAL NOT NULL,
        FOREIGN KEY (id_signal) REFERENCES signal(id) ON DELETE CASCADE,
        UNIQUE(id_indicator,id_signal, interval, params_name, value)
    );""")

    # Not complete
    cursor.execute("""CREATE TABLE IF NOT EXISTS strategy ( 
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        UNIQUE(name)    
    );""")

    # cursor.execute("""CREATE TABLE IF NOT EXISTS strategy_signal( 
    #     id_strategy INTEGER NOT NULL,
    #     id_signal INTEGER NOT NULL,
    #     PRIMARY KEY(id_signal,id_indicator),
    #     FOREIGN KEY (id_strategy) REFERENCES strategy(id) ON DELETE CASCADE,
    #     FOREIGN KEY (id_strategy_signal) REFERENCES signal(id) ON DELETE CASCADE
    # );""")

    # cursor.execute("""CREATE TABLE IF NOT EXISTS coin_strategy (   
    #     id_coin_pair INTEGER NOT NULL,
    #     id_strategy INTEGER NOT NULL,
    #     PRIMARY KEY(id_symbol , id_strategy),
    #     FOREIGN KEY (id_strategy) REFERENCES strategy(id) ON DELETE CASCADE,
    #     FOREIGN KEY (id_coin_pair) REFERENCES coin_pair(id) ON DELETE CASCADE
    # );""")

    # cursor.execute("""CREATE TABLE IF NOT EXISTS order(   
    #     id INTEGER PRIMARY KEY AUTOINCREMENT,
    #     id_strategy INTEGER NOT NULL,
    #     time TIMESTAMP NOT NULL,
    #     symbol TEXT NOT NULL,
    #     price NOT NULL,
    #     amount NOT NULL,
    #     type TEXT NOT NULL, 
    #     status TEXT NOT NULL, 
    #     FOREIGN KEY (id_strategy) REFERENCES strategy(id) ON DELETE CASCADE
    # );""")

    # cursor.execute("""CREATE TABLE IF NOT EXISTS wallet(   
    #     id INTEGER PRIMARY KEY AUTOINCREMENT,
    #     id_strategy INTEGER NOT NULL,
    #     balance NOT NULL, 
    #     FOREIGN KEY (id_strategy) REFERENCES strategy(id) ON DELETE CASCADE
    # );""")

    # cursor.execute("""CREATE TABLE IF NOT EXISTS wallet_coin(   
    #     id_wallet INTEGER NOT NULL,
    #     coin_name TEXT,
    #     amount NOT NULL, 
    #     PRIMARY KEY(id_wallet,coin_name),
    #     FOREIGN KEY (id_wallet) REFERENCES wallet(id) ON DELETE CASCADE
    # );""")





    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_db()