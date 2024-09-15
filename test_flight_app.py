import unittest
from unittest.mock import patch

import pandas as pd
from flight_app import calculate_success, app
import json

class TestFlightApp(unittest.TestCase):

    def setUp(self):
        # Sample DataFrame to simulate the CSV data
        self.df = pd.DataFrame({
            'flight ID': ['A12', 'A14', 'B15', 'C124', 'C23'],
            'Arrival': ['09:00', '12:00', '10:00', '14:00', '08:00'],
            'Departure': ['13:00', '19:00', '13:00', '16:00', '17:00'],
            'success': [''] * 5
        })

    def test_success_calculation(self):
        # Run the success calculation
        processed_df = calculate_success(self.df)

        # Check if the success column was calculated correctly
        self.assertEqual(processed_df.at[0, 'success'], 'success')  # A12: 4-hour flight, should be success
        self.assertEqual(processed_df.at[1, 'success'], 'success')  # A14: 7-hour flight, should be success
        self.assertEqual(processed_df.at[2, 'success'],
                         'success')  # B15: 3-hour flight, should be success (exactly 180 minutess)
        self.assertEqual(processed_df.at[3, 'success'], 'fail')  # C124: 2-hour flight, should be fail
        self.assertEqual(processed_df.at[4, 'success'], 'success')  # C23: 9-hour flight, should be success

    def test_flight_order(self):
        # Run the success calculation
        processed_df = calculate_success(self.df)

        # Check that the flights are sorted by arrival time
        self.assertEqual(list(processed_df['flight ID']), ['C23', 'A12', 'B15', 'A14', 'C124'])


class TestFlightAPI(unittest.TestCase):

    def setUp(self):
        # Create a test client for the Flask app
        self.app = app.test_client()
        self.app.testing = True

        # Sample data to simulate the CSV
        self.sample_data = [
            {'flight ID': 'A12', 'Arrival': '09:00', 'Departure': '13:00', 'success': 'success'},
            {'flight ID': 'A14', 'Arrival': '12:00', 'Departure': '19:00', 'success': 'success'}
        ]

    def test_get_flight(self):
        # Simulate a GET request for flight A12
        response = self.app.get('/flight/A12')

        # Parse the JSON response
        data = json.loads(response.get_data(as_text=True))

        # Test the response data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['flight ID'], 'A12')
        self.assertEqual(data['success'], 'success')

    def test_get_non_existent_flight(self):
        # Simulate a GET request for a flight that doesn't exist
        response = self.app.get('/flight/B99')

        # Test the response
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['error'], 'Flight not found')

    @patch('pandas.DataFrame.to_csv')
    def test_post_update_flights(self, mock_to_csv):
        # Prepare the data to send in the POST request
        new_flights = {
            "flights": [
                {"flight ID": "A20", "Arrival": "10:00", "Departure": "13:00", "success": ""},
                {"flight ID": "B30", "Arrival": "11:00", "Departure": "15:00", "success": ""}
            ]
        }

        # Send a POST request to update flights
        response = self.app.post(
            '/update_flights',
            data=json.dumps(new_flights),
            content_type='application/json'
        )

        # Assert that the response is correct
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "Flights updated successfully"})

        # Ensure that the CSV file was attempted to be updated
        mock_to_csv.assert_called_once_with('flights.csv', index=False)

    def test_post_invalid_flights(self):
        # Test POST request with invalid data (missing 'flights' key)
        response = self.app.post('/update_flights',
                                 data=json.dumps({}),
                                 content_type='application/json')

        # Check for error response
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['error'], 'No flight data provided')

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
