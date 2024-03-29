#db.py
import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

# Database initialization
db_file = 'trips.db'
conn = create_connection(db_file)

if conn is not None:
    # Create trips table
    create_trips_table_sql = """ CREATE TABLE IF NOT EXISTS trips (
                                        id integer PRIMARY KEY,
                                        start TEXT NOT NULL,
                                        end TEXT NOT NULL,
                                        distance TEXT,
                                        duration TEXT
                                    ); """
    create_table(conn, create_trips_table_sql)
else:
    print("Error! cannot create the database connection.")

def insert_trip(start, end, distance, duration):
    """
    Insert a new trip into the trips table
    """
    conn = create_connection(db_file)
    sql = ''' INSERT INTO trips(start, end, distance, duration)
              VALUES(?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, (start, end, distance, duration))
    conn.commit()
    conn.close()

def get_trips():
    """
    Query all rows in the trips table
    """
    conn = create_connection(db_file)
    cur = conn.cursor()
    cur.execute("SELECT * FROM trips")

    rows = cur.fetchall()

    conn.close()
    return rows


conn.close()
