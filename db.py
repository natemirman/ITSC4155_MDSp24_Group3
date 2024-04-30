#db.py
import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """ 
    Create a database connection to a SQLite database file.
    
    Args:
    db_file (str): The path to the SQLite database file.
    
    Returns:
    conn: The database connection object.
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn

def create_table(conn, create_table_sql):
    """ 
    Create a table in the database using the provided SQL statement.
    
    Args:
    conn: The database connection object.
    create_table_sql (str): The SQL statement to create the table.
    """
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
                                        stop TEXT NOT NULL,
                                        distance TEXT,
                                        duration TEXT
                                    ); """
    create_table(conn, create_trips_table_sql)
else:
    print("Error! cannot create the database connection.")
if conn is not None:
    # Create trips table
    create_trips_table_sql = """ CREATE TABLE IF NOT EXISTS packing_list (
                                        id INTEGER PRIMARY KEY,
                                        trip_id INTEGER NOT NULL,
                                        item TEXT NOT NULL,
                                        FOREIGN KEY (trip_id) REFERENCES trips (id)
                                    ); """
    create_table(conn, create_trips_table_sql)
else:
    print("Error! cannot create the database connection.")

def insert_trip(start, end, distance, duration,stop):
    """
    Insert a new trip into the trips table.
    
    Args:
    start (str): The starting location of the trip.
    end (str): The ending location of the trip.
    distance (str): The distance of the trip.
    duration (str): The duration of the trip.
    stop (str): Any stops made during the trip.
    """
    conn = create_connection(db_file)
    sql = ''' INSERT INTO trips(start, end, distance, duration,stop)
              VALUES(?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, (start, end, distance, duration,stop))
    conn.commit()
    conn.close()

def get_trips():
    """
    Query all rows in the trips table.
    
    Returns:
    list: A list of tuples representing each row in the trips table.
    """
    conn = create_connection(db_file)
    cur = conn.cursor()
    cur.execute("SELECT * FROM trips")

    rows = cur.fetchall()

    conn.close()
    return rows
def get_trip_by_id(trip_id):
    """
    Query a trip by its ID.
    
    Args:
    trip_id (int): The ID of the trip to retrieve.
    
    Returns:
    tuple: A tuple representing the row in the trips table corresponding to the provided trip ID.
    """
    conn = create_connection(db_file)
    cur = conn.cursor()
    cur.execute("SELECT * FROM trips WHERE id=?", (trip_id,))
    
    row = cur.fetchone()
    
    conn.close()
    return row
def delete_trip(trip_id):
    """
    Delete a trip by its ID.
    
    Args:
    trip_id (int): The ID of the trip to delete.
    """
    conn = create_connection(db_file)
    cur = conn.cursor()
    cur.execute("DELETE FROM trips WHERE id=?", (trip_id,))
    conn.commit()
    conn.close()


def insert_packing_list_item(trip_id, item):
    """
    Insert a new packing list item into the database for a specific trip.
    
    Args:
    trip_id (int): The ID of the trip.
    item (str): The packing list item to insert.
    """
    conn = create_connection(db_file)
    sql = ''' INSERT INTO packing_list(trip_id, item)
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, (trip_id, item))
    conn.commit()
    conn.close()

def get_packing_list(trip_id):
    """
    Retrieve the packing list items for a specific trip.
    
    Args:
    trip_id (int): The ID of the trip.
    
    Returns:
    list: A list of packing list items for the specified trip.
    """
    conn = create_connection(db_file)
    cur = conn.cursor()
    cur.execute("SELECT item FROM packing_list WHERE trip_id=?", (trip_id,))
    
    rows = cur.fetchall()
    
    conn.close()
    return [row[0] for row in rows]

def delete_item(trip_id, item):
    """
    Delete item
    
    Args:
    trip_id (int): The ID of the trip to delete.
    item (str): The packing list item to insert.

    """
    conn = create_connection(db_file)
    cur = conn.cursor()
    cur.execute("DELETE FROM packing_list WHERE trip_id=? AND item=?", (trip_id,item,))
    conn.commit()
    conn.close()


conn.close()

