from flask import Flask, request, session, redirect, url_for, render_template, flash, g
from db import add_user, verify_user, get_db

app = Flask(__name__)
app.secret_key = 'your_very_secret_key'  # Set to a secure, random secret key in production

# Index route to check if a user is logged in and redirect accordingly
@app.route('/')
def index():
    if 'user_id' in session:
        return render_template('index.html', user=session['username'])
    return redirect(url_for('login'))

# Route for user registration
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        try:
            add_user(username, email, password)
            flash('User successfully registered. Please log in.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            flash('Error registering user. User may already exist.', 'error')
    return render_template('signup.html')

# Route for user login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')  # Use .get() to avoid BadRequestKeyError
        password = request.form.get('password')
        if verify_user(email, password):
            session['user_id'] = email  # Storing user email as identifier in session
            session['username'] = email.split('@')[0]  # Example to use part of the email as username
            flash('You were successfully logged in', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid email/password combination', 'error')
    return render_template('login.html')

# Route for logging out a user
@app.route('/logout')
def logout():
    session.pop('user_id', None)  # Remove the user_id from session
    session.pop('username', None)  # Remove the username from session
    flash('You were logged out', 'success')
    return redirect(url_for('login'))

# Ensure that database connections are closed
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

if __name__ == '__main__':
    app.run(debug=True)
<<<<<<< HEAD
=======

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/stat')
def see_stats():
    trips = db.get_trips()  # Assuming this fetches all trips data
    total_distance = db.get_total_distance()
    total_time = db.get_total_time()
    total_trips = db.get_total_trips()
    flags = db.get_flags()
    return render_template('stat.html', trips=trips, total_distance=total_distance, total_time=total_time, total_trips=total_trips, flags=flags)
>>>>>>> main
