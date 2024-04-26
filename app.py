#__init__.py
from flask import Flask, request, redirect, render_template
import db

app = Flask(__name__)
#Renders the index.html template, which serves as the homepage of the application.
@app.route('/')
def index():
    return render_template('index.html')

#Handles both GET and POST requests to plan a trip.

#If the request method is POST, it extracts form data (start, end, distance, duration, stop) 
#and inserts it into the database using the insert_trip() function from db.py.

#If the request method is GET, it renders the plan.html templete
@app.route('/plan', methods=['GET', 'POST'])
def plan_trip():
    if request.method == 'POST':
        start = request.form['start']
        end = request.form['end']
        distance = request.form['distance'] 
        duration = request.form['duration'] 
        stop=request.form['stop']

        db.insert_trip(start, end, distance, duration,stop)
        return redirect('/see')
    else:
        return render_template('plan.html')


#Retrieves information for all trips from the database using the get_trips() function from db.py

#Renders the view_database.html template, passing the retrieved trips data to it for display.
@app.route('/see')
def see_trips():
    trips = db.get_trips()
    return render_template('view_database.html', trips=trips)


#Fetches trip details from the database based on the provided trip_id using 
#the get_trip_by_id() function from db.py.

#Renders the view.html template, passing the retrieved trip data to it for display.
@app.route('/view/<int:trip_id>')
def view_trip(trip_id):
    trip = db.get_trip_by_id(trip_id) 
    return render_template('view.html', trip=trip)

#Deletes a trip from the database based on the provided trip_id using the delete_trip() function from db.py.

#Retrieves information for all trips from the database using the get_trips() function from db.py.

#Renders the view_database.html template, passing the updated trips data to it for display.
@app.route('/delete/<int:trip_id>')
def delete_trips(trip_id):
    trips = db.delete_trip(trip_id)
    trips = db.get_trips()
    return render_template('view_database.html', trips=trips)

if __name__ == '__main__':
    app.run(debug=True)
