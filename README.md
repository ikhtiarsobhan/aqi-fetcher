# aqi-fetcher
# FIND SOME FRESH AIR
This project get the Air Quality Index (AQI) and relevant weather data of the user's current location.

#### Video Demo:  <URL HERE>
#### Description: This project gets the Air Quality Index (AQI) and relevant weather data of the user's current location. It uses the AirVisual API. The program find the user's current location based on their IP address and then uses that information to get the AQI data for the nearest city. It then displays the information in a user-friendly format in the CLI. The data is also saved to a CSV file for further analysis.

## Prerequisites
- Python 3.x
- `requests` library
- `pandas` library
- A valid AirVisual API key

## Installation
1. Clone this repository:
   ```sh
   git clone https://github.com/ikhtiarsobhan/aqi-fetcher.git
   ```
2. Navigate to the project directory:
   ```sh
   cd aqi-fetcher
   ```
3. Install the required libraries:
   ```sh
   pip install requests pandas
   ```

## Configuration
1. Create a `config.json` file in the project directory with the following structure:
   ```json
   {
       "api_key": "your_airvisual_api_key"
   }
   ```

## Usage
1. Run the script:
   ```sh
   python project.py
   ```

## Functions

### `load_api_key()`
Loads the API key from the `config.json` file. The user needs to get an API Key by registering at https://www.iqair.com/. The config.json file has a single line with a dictionary format "api_key": "Your API Key Here". The user need to edit the config.json file and replace "Your API Key Here" with the collected API key. Remember to surround the API Key with the quotation marks ("). Example of a file is - 
      {
          "api_key": "84be77eb-f6e5-49c9-9708-3238a664254a"
      }  


### `get_user_location()`
This function gets the user's current location (latitude and longitude) using their current IP address. If a user uses a VPN, this may produce wrong results.

### `fetch_data(lat, lon, api_key)`
Gets the air quality and relevant weather data for the nearest city based on the provided latitude, and longitude. The function gets the AQI, Main Pollutant, Temperature (in Celcius), Humidity, and Wind Speed (in m/s).

### `get_aqi_description(aqi)`
Since the actual Air Quality Index (AQI) values are not easy to understand, this function returns a textual description of the air quality based on the AQI value.

### `display_and_save_data(data)`
This function displays the data on the screen, in CLI interface, and also saves it to a CSV file in the current directory.

### `main()`
This function consolidates everything and executes the code.


## Example Output
```
Air Quality Index (AQI) in City, State, Country:
- AQI: 75 (Moderate)
- Main Pollutant: pm2_5
- Temperature: 22°C
- Humidity: 56%
- Wind Speed: 3 m/s

Air Quality Descriptions:
0-50: Good
51-100: Moderate
101-150: Unhealthy for Sensitive Groups
151-200: Unhealthy
201-300: Very Unhealthy
301+: Hazardous
```

## License
This project is licensed under the MIT License.
