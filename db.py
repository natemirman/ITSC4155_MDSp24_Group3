#db.py
import sqlite3
from sqlite3 import Error
from flask import app, g
from werkzeug.security import generate_password_hash, check_password_hash

#New user session methods:
################################################
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('trips.db')
        db.row_factory = sqlite3.Row
    return db

def add_user(username, email, password):
    db = get_db()
    db.execute("INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
               [username, email, generate_password_hash(password)])
    db.commit()

def verify_user(email, password):
    db = get_db()
    user = db.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
    print("User fetched:", user)  # Check what user data is fetched
    if user:
        print("Password hash:", user['password_hash'])  # This should show the hash
        return check_password_hash(user['password_hash'], password)
    return False


#End of the user session methods
##################################################


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
                                        stop TEXT NOT NULL,
                                        distance TEXT,
                                        duration TEXT
                                    ); """
    create_table(conn, create_trips_table_sql)
else:
    print("Error! cannot create the database connection.")

def insert_trip(start, end, distance, duration,stop):
    """
    Insert a new trip into the trips table
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
    Query all rows in the trips table
    """
    conn = create_connection(db_file)
    cur = conn.cursor()
    cur.execute("SELECT * FROM trips")

    rows = cur.fetchall()

    conn.close()
    return rows
def get_trip_by_id(trip_id):
    """
    Query a trip by its ID
    """
    conn = create_connection(db_file)
    cur = conn.cursor()
    cur.execute("SELECT * FROM trips WHERE id=?", (trip_id,))
    
    row = cur.fetchone()
    
    conn.close()
    return row
def delete_trip(trip_id):
    """
    Delete a trip by its ID
    """
    conn = create_connection(db_file)
    cur = conn.cursor()
    cur.execute("DELETE FROM trips WHERE id=?", (trip_id,))
    conn.commit()
    conn.close()


conn.close()
