import sqlite3

DB_FILE = "weather.db"

def get_connection():
    #open new connection to file with each call
    return sqlite3.connect(DB_FILE)

def initalize_db():
    with get_connection() as connection:
        cursor = connection.cursor()

        #create queries table if nonexistent (display, coordinates, date range)
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS queries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            label TEXT, 
            lat REAL,
            lon REAL,
            start_date TEXT,
            end_date TEXT,  
        )
        ''')
        cursor.commit()

def create_query(label, lat, lon, start_date=None, end_date=None):
    with get_connection() as connection:
        cursor = connection.cursor()

        #create new row storing new request (location + date range)
        cursor.execute('''
            INSERT INTO queries 
            (label, lat, lon, start_date, end_date) VALUES (?,?,?,?,?),
            (label, lat, lon, start_date, end_date),    
        ''')
        cursor.commit()
        return cursor.lastrowid

def read_queries():
    with get_connection() as connection:
        cursor = connection.cursor()

        #READ endpoint via all rows saved as a list
        cursor.execute('SELECT * FROM queries')
        return cursor.fetchall()


def update_query(query_id, start_date, end_date):
    with get_connection() as connection:
        cursor = connection.cursor()

        #update date range of saved query
        cursor.execute(
            'UPDATE queries SET start_date = ?, end_date = ? WHERE id = ?',
            (start_date, end_date, query_id)
        )
        cursor.commit()
        return cursor.rowcount

def delete_query(query_id):
    with get_connection() as connection:
        cursor = connection.cursor()

        #delete row based on id
        cursor.execute(
            'DELETE FROM queries WHERE id = ?', (query_id,)
        )
        cursor.commit()
        return cursor.rowcount