# Flight Success Tracker API

## Overview

This project provides an API to track flight schedules, calculate whether a flight was successful based on specific conditions, and update the flight schedule. The success of a flight is determined by two factors:
1. The flight duration (time between arrival and departure) must be at least 180 minutes.
2. No more than 20 successful flights can occur in one day.

### Features
- **GET**: Retrieve flight information based on flight ID.
- **POST**: Update the flight schedule by adding new flight entries.
- Automatically calculates whether each flight is successful or not.

---

## Requirements

- Python 3.x
- Flask (`pip install Flask`)
- Pandas (`pip install pandas`)

### Optional: Install requirements via pip:
```bash
pip install -r requirements.txt
```

# Running the Application
Run the Flask API:

```bash
python flight_app.py
```
The application will start on http://127.0.0.1:5000/.

# Endpoints
## 1. GET /flight/{flight_id}
Retrieve flight information by flight ID.

URL: /flight/<flight_id></br>
Method: GET</br>
Response:</br>
Success: Returns a JSON object containing the flight details.</br>
Failure: Returns a 404 if the flight ID does not exist.</br>

### Example Request:
```bash
GET /flight/A12
```
### Example Response:
```bash
{
    "flight ID": "A12",
    "Arrival": "09:00",
    "Departure": "13:00",
    "success": "success"
}
```
## 2. POST /update_flights
Add or update the flight schedule.

URL: /update_flights</br>
Method: POST</br>
Request Body (JSON):</br>
flights: A list of flight objects with flight ID, Arrival, Departure, and success fields.

### Example Request:

```bash
{
  "flights": [
    {"flight ID": "A20", "Arrival": "10:00", "Departure": "13:00", "success": ""},
    {"flight ID": "B30", "Arrival": "11:00", "Departure": "15:00", "success": ""}
  ]
}
```
### Example Response:
```bash
{
  "message": "Flights updated successfully"
}
```

# Running Tests
The project uses unittest for testing.

Run the tests:

```bash
python -m unittest test_flight_app.py
```
The test file (test_flight_app.py) includes:

Unit tests to validate the flight success calculation.
API tests to ensure the GET and POST endpoints work correctly.