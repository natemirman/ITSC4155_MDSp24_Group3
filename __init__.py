#__init__.py
from flask import Flask, request, redirect, render_template
import db  # Ensure this imports your db.py functionality for database interaction

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/plan', methods=['GET', 'POST'])
def plan_trip():
    if request.method == 'POST':
        # Extract form data
        start = request.form['start']
        end = request.form['end']
        distance = request.form['distance']  # Assuming you add a way to input this in the form
        duration = request.form['duration']  # Assuming you add a way to input this in the form
        
        # Assuming db.py has a function called insert_trip that inserts the data into the database
        db.insert_trip(start, end, distance, duration)
        
        # Redirect to another page, maybe to the list of trips
        return redirect('/see')
    else:
        return render_template('plan.html')

@app.route('/see')
def see_trips():
    # Assuming db.py has a function called get_trips that fetches trips from the database
    trips = db.get_trips()
    return render_template('view_database.html', trips=trips)

@app.route('/view/<int:trip_id>')
def view_trip(trip_id):
    # Fetch trip details from the database based on trip_id
    trip = db.get_trip_by_id(trip_id)

    
    return render_template('view.html', trip=trip)

if __name__ == '__main__':
    app.run(debug=True)
