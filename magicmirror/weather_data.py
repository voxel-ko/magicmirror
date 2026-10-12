import json
import time
from functools import lru_cache
import logging

import requests

from . import config

logger = logging.getLogger(__name__)

def get_geolocation() -> tuple[int, int, str]:
    """
    :return: A tuple containing latitude, longitude, and timezone of the server obtained from its public IP address
    """
    url = "http://ip-api.com/json"  # Can't use SSL/HTTPS without paying, it worked before for some reason

    request = requests.get(url)
    request_json = request.json()

    latitude = request_json.get("lat", 0)
    longitude = request_json.get("lon", 0)
    timezone = request_json.get("timezone", "utc")

    return latitude, longitude, timezone


# Used to ensure that get_weather_data() only changes every 15 minutes
def get_ttl_hash(seconds=900):
    return round(time.time() / seconds)


@lru_cache(maxsize=1)
def get_weather_data(ttl_hash=None):
    """
    Calls open-meteo's API to get weather data and then formats it as a JSON object

    :param logger: An optional logger to log when API calls happen
    :param ttl_hash: Used to ensure that the cache updates every 15 minutes to avoid API rate limiting
    :return: A JSON object containing data about the current weather
    """
    del ttl_hash
    logger.info("Weather API - Calling Open Meteo")

    url = "https://api.open-meteo.com/v1/forecast"

    latitude, longitude = config.config.latitude, config.config.longitude
    wind_speed_unit = config.config.speed_unit
    temperature_unit = config.config.temperature_unit

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": ["temperature_2m", "precipitation", "relative_humidity_2m", "wind_speed_10m"],
        "timezone": "auto",
        "wind_speed_unit": wind_speed_unit,
        "forecast_days": 1,
        "temperature_unit": temperature_unit
    }

    request = requests.get(url, params=params)
    request_json = request.json()

    return json.dumps({
        "temperature": request_json["current"]["temperature_2m"],
        "temperature_unit": f"°{params['temperature_unit'][0].upper()}",
        "precipitation": request_json["current"]["precipitation"],
        "relative_humidity_2m": request_json["current"]["relative_humidity_2m"],
        "wind_speed_10m": request_json["current"]["wind_speed_10m"]
    })
