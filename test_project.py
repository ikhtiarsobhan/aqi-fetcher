import unittest
from unittest.mock import patch, mock_open
import json
import requests
import pandas as pd
from io import StringIO

# Import functions from the original script
from your_script import load_api_key, get_user_location, fetch_data, get_aqi_description, display_and_save_data

class TestAirQualityScript(unittest.TestCase):
    
    @patch("builtins.open", new_callable=mock_open, read_data='{"api_key": "test_api_key"}')
    def test_load_api_key(self, mock_file):
        self.assertEqual(load_api_key(), "test_api_key")
    
    @patch("builtins.open", side_effect=FileNotFoundError)
    def test_load_api_key_file_not_found(self, mock_file):
        self.assertIsNone(load_api_key())

    @patch("requests.get")
    def test_get_user_location(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"loc": "23.8103,90.4125"}
        lat, lon = get_user_location()
        self.assertEqual(lat, "23.8103")
        self.assertEqual(lon, "90.4125")
    
    @patch("requests.get", side_effect=requests.exceptions.RequestException("API error"))
    def test_get_user_location_failure(self, mock_get):
        lat, lon = get_user_location()
        self.assertIsNone(lat)
        self.assertIsNone(lon)

    @patch("requests.get")
    def test_fetch_data(self, mock_get):
        mock_response = {
            "data": {
                "city": "Dhaka",
                "state": "Dhaka",
                "country": "Bangladesh",
                "current": {
                    "pollution": {"aqius": 150, "mainus": "pm2.5"},
                    "weather": {"tp": 30, "hu": 60, "ws": 3}
                }
            }
        }
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response
        data = fetch_data("23.8103", "90.4125", "test_api_key")
        self.assertEqual(data, mock_response)
    
    @patch("requests.get", side_effect=requests.exceptions.RequestException("API error"))
    def test_fetch_data_failure(self, mock_get):
        data = fetch_data("23.8103", "90.4125", "test_api_key")
        self.assertIsNone(data)

    def test_get_aqi_description(self):
        self.assertEqual(get_aqi_description(30), "Good")
        self.assertEqual(get_aqi_description(75), "Moderate")
        self.assertEqual(get_aqi_description(125), "Unhealthy for Sensitive Groups")
        self.assertEqual(get_aqi_description(175), "Unhealthy")
        self.assertEqual(get_aqi_description(250), "Very Unhealthy")
        self.assertEqual(get_aqi_description(350), "Hazardous")

    @patch("builtins.print")
    @patch("pandas.DataFrame.to_csv")
    def test_display_and_save_data(self, mock_to_csv, mock_print):
        data = {
            "data": {
                "city": "Dhaka",
                "state": "Dhaka",
                "country": "Bangladesh",
                "current": {
                    "pollution": {"aqius": 150, "mainus": "pm2.5"},
                    "weather": {"tp": 30, "hu": 60, "ws": 3}
                }
            }
        }
        display_and_save_data(data)
        mock_to_csv.assert_called_once()
        mock_print.assert_called()

if __name__ == "__main__":
    unittest.main()
