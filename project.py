import requests
import json
import pandas as pd

# Function to load API key from config.json
def load_api_key():
    try:
        with open('config.json') as config_file:
            config = json.load(config_file)
        return config.get('api_key')
    except (FileNotFoundError, json.JSONDecodeError):
        print("Error: config.json file is missing or invalid.")
        return None

# Function to get the user's current location (latitude & longitude)
def get_user_location():
    try:
        response = requests.get("https://ipinfo.io/json")
        response.raise_for_status()
        location_data = response.json()
        lat, lon = map(str, location_data["loc"].split(','))
        return lat, lon
    except requests.exceptions.RequestException as e:
        print(f"Error fetching location: {e}")
        return None, None

# Function to fetch air quality data based on nearest city
def fetch_data(lat, lon, api_key):
    url = f"https://api.airvisual.com/v2/nearest_city?lat={lat}&lon={lon}&key={api_key}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        if 'data' not in data:
            print("Error: No data found for this location.")
            return None
        
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

# Function to get air quality description based on AQI
def get_aqi_description(aqi):
    if aqi <= 50:
        return "Good"
    elif aqi <= 100:
        return "Moderate"
    elif aqi <= 150:
        return "Unhealthy for Sensitive Groups"
    elif aqi <= 200:
        return "Unhealthy"
    elif aqi <= 300:
        return "Very Unhealthy"
    else:
        return "Hazardous"

# Function to display and save data
def display_and_save_data(data):
    if not data:
        print("No valid data to display.")
        return

    city = data['data']['city']
    state = data['data']['state']
    country = data['data']['country']
    pollution = data['data']['current']['pollution']
    weather = data['data']['current']['weather']

    air_quality = pollution['aqius']
    main_pollutant = pollution['mainus']
    temperature = weather['tp']
    humidity = weather['hu']
    wind_speed = weather['ws']
    aqi_description = get_aqi_description(air_quality)

    result_text = f"""
    Air Quality Index (AQI) in {city}, {state}, {country}:
    - AQI: {air_quality} ({aqi_description})
    - Main Pollutant: {main_pollutant}
    - Temperature: {temperature}°C
    - Humidity: {humidity}%
    - Wind Speed: {wind_speed} m/s

    Air Quality Descriptions:
    0-50: Good
    51-100: Moderate
    101-150: Unhealthy for Sensitive Groups
    151-200: Unhealthy
    201-300: Very Unhealthy
    301+: Hazardous
    """
    print(result_text)

    # Save data to CSV
    df = pd.DataFrame([{
        "City": city,
        "State": state,
        "Country": country,
        "AQI": air_quality,
        "Main Pollutant": main_pollutant,
        "Temperature (°C)": temperature,
        "Humidity (%)": humidity,
        "Wind Speed (m/s)": wind_speed
    }])
    df.to_csv("air_quality.csv", index=False)
    print(f"Data saved to air_quality.csv\n\n")

# Main function
def main():
    api_key = load_api_key()
    if not api_key:
        return

    lat, lon = get_user_location()
    if not lat or not lon:
        print("Could not determine your location. Please try again.")
        return

    data = fetch_data(lat, lon, api_key)
    display_and_save_data(data)

if __name__ == "__main__":
    main()
