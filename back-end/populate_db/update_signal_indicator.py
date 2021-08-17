import sys
sys.path.append('../')
import signals 
import sqlite3 as sql
import config

def update_indicator(indicators, id_signal):
    conn = sql.connect(config.DB_URL)
    conn.row_factory = sql.Row
    cursor = conn.cursor()

    for indicator in indicators:
        select_query = '''INSERT OR REPLACE INTO indicator(id_indicator, id_signal, interval, params_name, value)
                        VALUES(?, ?, ?, ?, ?) '''
        id_indicator = indicator['id']
        interval = indicator['interval']
        inputs = indicator['inputs']
        
        for params_name in inputs:
            value = inputs[params_name]
            cursor.execute(select_query, (id_indicator, id_signal, interval, params_name, value,))
            print(f'Add new {id_indicator}!')

    conn.commit()
    conn.close()

def update_signal_indicator():
    conn = sql.connect(config.DB_URL)
    conn.row_factory = sql.Row
    cursor = conn.cursor()


    for sn in signals.SIGNALS:
        indicators = sn.getIndicator()
        name = sn.getName()
        select_query = '''SELECT name FROM signal where name = (?) '''
        cursor.execute(select_query, (name,))
        result = cursor.fetchone()
        
        # Check signal existed
        if result == None:
            select_query = '''INSERT OR REPLACE INTO signal(name) VALUES(?) '''
            cursor.execute(select_query, (name,))
            print(f'New signal {name} added!')
        else:
           name = result['name']
           print(f'{name} already in table!') 

        select_query = '''SELECT id FROM signal where name = (?) '''
        cursor.execute(select_query, (name,))
        result  = cursor.fetchone()
        id_signal = result['id']
        update_indicator(indicators, id_signal)
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    update_signal_indicator()