# Road Trip
The Travel Planner is a web application designed to help users plan and manage their road trips efficiently.

## Key Features
Trip Planning: Users can input start and end locations, as well as optional stopovers, to plan their trips.

Route Calculation: The application uses the Google Maps API to calculate the route between the specified locations, including any stopovers.

Distance and Duration: The distance and duration of the trip are calculated and displayed to the user.

Trip Management: Users can save their planned trips to the database for future reference.

View and Delete Trips: Users can view a list of their planned trips, including details such as start and end locations, distance, and duration. They can also delete trips if needed.

## app.py:
-Main Python script for the web application.
-Defines routes and corresponding functions using Flask.
-Handles rendering HTML templates, processing form data, interacting with the database, and serving API endpoints.

## db.py:
-Python script for interacting with the SQLite database (trips.db).
-Defines functions for creating a database connection, creating tables, inserting, retrieving, and deleting trip records.
-Initializes the database and closes connections when necessary.

## trips.db:
-SQLite database file storing trip records.
-Contains tables and rows representing planned trips, including start, end, stop, distance, and duration.

## templates/index.html:
-HTML template for the home page.
-Includes a navigation bar, header, and buttons for logging in and signing up.
-Provides links to other pages such as plan and see trips

## templates/plan.html:
-HTML template for planning a new trip.
-Includes a form with inputs for start, end, and stop locations, as well as buttons for calculating the route and saving the trip.
-Uses hidden inputs to store calculated distance and duration values.
-Includes a map display using Google Maps JavaScript API.

## templates/see.html:
-HTML template for displaying a list of all planned trips.
-Includes a table with columns for trip ID, start, end, distance, duration, and action buttons for viewing and deleting trips.
Provides a button to plan a new trip.

## templates/view.html:
HTML template for viewing details of a specific trip.
Includes a map display showing the route, as well as information about the trip such as distance and time.
Displays direction steps below the map.

## templates/about.html:
Not yet finished
## templates/contact.html
Not yet finished
## templates/stats.html
Not yet finished

## static/roadtrip.jpg:
Image file in the index.html template.

## To run the applicaton: run python app.py
