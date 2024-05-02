import sqlite3
from werkzeug.security import generate_password_hash

def create_db():
    conn = sqlite3.connect('trips.db')  # Adjust the path if different
    cursor = conn.cursor()

    # Create the users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL
    );
    ''')

    # Check if the admin user already exists to avoid duplicate entries
    cursor.execute('SELECT * FROM users WHERE username="admin"')
    if cursor.fetchone() is None:
        # Define the user data
        username = "admin"
        email = "admin@seniorproject.com"
        password = "admin1234"  # Plain text password for hash generation
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')


        # Insert the predefined user 'admin'
        cursor.execute('''
        INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)
        ''', (username, email, hashed_password))
    

    conn.commit()  # Commit changes to the database
    conn.close()  # Close the database connection

if __name__ == '__main__':
    create_db()
    print("Database setup complete with initial data.")
