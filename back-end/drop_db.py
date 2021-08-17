import sqlite3 as sql
import config 

def drop_db():
    conn = sql.connect(config.DB_URL)

    cursor = conn.cursor()

    #drop coin_pair
    cursor.execute("""DROP TABLE IF EXISTS coin_pair; """)

    #drop coin_price
    cursor.execute("""DROP TABLE IF EXISTS coin_price; """)

    conn.commit()
    conn.close()

if __name__ == '__main__':
    drop_db()