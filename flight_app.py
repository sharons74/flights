from flask import Flask, jsonify, request
import pandas as pd
from datetime import datetime, timedelta

app = Flask(__name__)

# Load the CSV data
csv_file = 'flights.csv'


# Helper function to calculate time difference in minutes
def time_diff_minutes(arrival, departure):
    FMT = '%H:%M'
    tdelta = datetime.strptime(departure, FMT) - datetime.strptime(arrival, FMT)
    return tdelta.total_seconds() / 60


# Helper function to calculate success for each flight
def calculate_success(df):
    # Sort flights by arrival time
    df['Arrival'] = pd.to_datetime(df['Arrival'], format='%H:%M')
    df.sort_values(by='Arrival', inplace=True)

    success_count = 0

    for i, row in df.iterrows():
        diff_minutes = time_diff_minutes(row['Arrival'].strftime('%H:%M'), row['Departure'])

        if diff_minutes >= 180 and success_count < 20:
            df.at[i, 'success'] = 'success'
            success_count += 1
        else:
            df.at[i, 'success'] = 'fail'

    df['Arrival'] = df['Arrival'].dt.strftime('%H:%M')
    return df


# Load and process CSV
def load_and_process_csv():
    df = pd.read_csv(csv_file)
    df = calculate_success(df)
    return df


# Endpoint to get flight info by flight ID
@app.route('/flight/<flight_id>', methods=['GET'])
def get_flight_info(flight_id):
    df = load_and_process_csv()
    flight_info = df[df['flight ID'] == flight_id].to_dict(orient='records')

    if flight_info:
        return jsonify(flight_info[0]), 200
    else:
        return jsonify({"error": "Flight not found"}), 404


# Endpoint to update CSV with new flight data
@app.route('/update_flights', methods=['POST'])
def update_flights():
    new_flights = request.json.get('flights', [])

    if not new_flights:
        return jsonify({"error": "No flight data provided"}), 400

    # Append new flight data to CSV
    df = pd.read_csv(csv_file)
    new_df = pd.DataFrame(new_flights)
    df = pd.concat([df, new_df], ignore_index=True)

    # Recalculate success and sort by arrival
    df = calculate_success(df)

    # Save updated CSV
    df.to_csv(csv_file, index=False)

    return jsonify({"message": "Flights updated successfully"}), 200


if __name__ == '__main__':
    app.run(debug=True)

    #df = load_and_process_csv()
    #print("calculated")