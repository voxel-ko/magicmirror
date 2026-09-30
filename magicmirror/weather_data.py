import datetime
import requests
import time
from functools import lru_cache
from flask import current_app

def get_hour():
    return int(datetime.datetime.now().strftime("%H"))

def get_geolocation():
    url = "http://ip-api.com/json"

    request = requests.get(url)
    request_json = request.json()

    latitude = request_json.get("lat", 0)
    longitude = request_json.get("lon", 0)

    return latitude, longitude

@lru_cache(maxsize=1)
def get_weather_data(*, ttl_hash=None):
    del ttl_hash
    current_app.logger.info("Weather API - Calling Open Meteo")

    url = "https://api.open-meteo.com/v1/forecast"

    latitude, longitude = get_geolocation()

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": ["temperature_2m", "precipitation", "relative_humidity_2m", "wind_speed_10m"],
        "timezone": "auto",
        "wind_speed_unit": "mph", # Don't add for km/h
        "forecast_days": 1,
        "temperature_unit": "fahrenheit" # Don't add if Celsius
    }

    request = requests.get(url, params=params)
    request_json = request.json()

    weather_data = {
        "temperature": request_json["current"]["temperature_2m"],
        "temperature_unit": f"°{params["temperature_unit"][0].upper()}",
        "precipitation": request_json["current"]["precipitation"],
        "relative_humidity_2m": request_json["current"]["relative_humidity_2m"],
        "wind_speed_10m": request_json["current"]["wind_speed_10m"]
    }

    return weather_data

def get_ttl_hash(seconds=900):
    return round(time.time() / seconds)

if __name__ == "__main__":
    print(get_weather_data(ttl_hash=get_ttl_hash()))
    print(get_weather_data(ttl_hash=get_ttl_hash()))
    print(get_weather_data(ttl_hash=get_ttl_hash()))
    print(get_weather_data(ttl_hash=get_ttl_hash()))
    print(get_weather_data(ttl_hash=get_ttl_hash()))