

CREATE TABLE TripData (
    RouteID INT PRIMARY KEY AUTO_INCREMENT,
    StartingDestination VARCHAR(255) NOT NULL,
    EndDestination VARCHAR(255) NOT NULL,
    StopDestination VARCHAR(255) NOT NULL,
    Distance INTEGER NOT NULL, 
    TripTime INTEGER NOT NULL, 
);
