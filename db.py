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
    
    
def get_total_distance():
    """
    Calculate the total distance of all trips in the trips table
    """
    conn = create_connection(db_file)
    cur = conn.cursor()
    cur.execute("SELECT SUM(Distance) FROM trips")
    total_distance = cur.fetchone()[0]  # Fetch the result which is the total distance
    conn.close()
    return round(total_distance, 2) if total_distance is not None else 0.0

def get_total_time():
    """
    Calculate the total time of all trips in the trips table, where duration is in the format 'X hr Y min'
    """
    conn = create_connection(db_file)
    cur = conn.cursor()
    cur.execute("SELECT duration FROM trips")
    durations = cur.fetchall()
    total_minutes = 0

    for duration in durations:
        if duration[0]:  # Check if duration is not None
            hours, minutes = parse_duration(duration[0])
            total_minutes += hours * 60 + minutes

    conn.close()
    return format_time(total_minutes)

def parse_duration(duration_str):
    """
    Parse the duration string 'X hr Y min' to get hours and minutes as integers
    """
    numbers = re.findall(r'\d+', duration_str)
    if len(numbers) == 2:
        return int(numbers[0]), int(numbers[1])  # hours, minutes
    elif 'hr' in duration_str:
        return int(numbers[0]), 0  # hours, no minutes
    elif 'min' in duration_str:
        return 0, int(numbers[0])  # no hours, minutes
    return 0, 0  # default if format is unexpected

def format_time(total_minutes):
    """
    Convert total minutes into days, hours, and minutes and format into a string
    """
    days = total_minutes // 1440
    hours = (total_minutes % 1440) // 60
    minutes = total_minutes % 60
    return f"{days} days, {hours} hours, {minutes} minutes"

def get_total_trips():
    """
    Calculate the total number of trips in the trips table
    """
    conn = create_connection(db_file)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM trips")  
    total_trips = cur.fetchone()[0]  
    return total_trips

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
    
def get_flags():
    """
    Query all rows in the trips table and check if columns start, stop, and end contain specific state identifiers.
    """
    states = [
        "AL, USA", "AK, USA", "AZ, USA", "AR, USA", "CA, USA",
        "CO, USA", "CT, USA", "DE, USA", "DC, USA", "FL, USA",
        "GA, USA", "HI, USA", "ID, USA", "IL, USA", "IN, USA",
        "IA, USA", "KS, USA", "KY, USA", "LA, USA", "ME, USA",
        "MD, USA", "MA, USA", "MI, USA", "MN, USA", "MS, USA",
        "MO, USA", "MT, USA", "NE, USA", "NV, USA", "NH, USA",
        "NJ, USA", "NM, USA", "NY, USA", "NC, USA", "ND, USA",
        "OH, USA", "OK, USA", "OR, USA", "PA, USA", "RI, USA",
        "SC, USA", "SD, USA", "TN, USA", "TX, USA", "UT, USA",
        "VT, USA", "VA, USA", "WA, USA", "WV, USA", "WI, USA", 
        "WY, USA"
    ]
    found_states = [False] * 51  # Initialize an array of 51 False values

    conn = create_connection(db_file)
    cur = conn.cursor()
    cur.execute("SELECT start, stop, end FROM trips")  # Modify to use the actual column names
    rows = cur.fetchall()

    for row in rows:
        for index, state in enumerate(states):
            if any(state in col for col in row):
                found_states[index] = True

    conn.close()
    return found_states


conn.close()
