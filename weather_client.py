# weather_client.py

import requests
from typing import List, Dict


OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"


def fetch_hourly_forecast(
    latitude: float,
    longitude: float,
    date: str
) -> List[Dict]:
    """
    Fetches hourly forecast data for a given location and date.
    Returns normalized data for heatwave risk analysis.
    """

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": [
            "temperature_2m",
            "relativehumidity_2m",
            "windspeed_10m"
        ],
        "timezone": "auto"
    }

    response = requests.get(OPEN_METEO_URL, params=params, timeout=10)
    response.raise_for_status()

    data = response.json()
    hourly = data.get("hourly", {})

    times = hourly.get("time", [])
    temperatures = hourly.get("temperature_2m", [])
    humidity = hourly.get("relativehumidity_2m", [])
    windspeed = hourly.get("windspeed_10m", [])

    normalized = []

    for i in range(len(times)):
        # Filter only requested date
        if not times[i].startswith(date):
            continue

        normalized.append({
            "time": times[i],
            "temperature": temperatures[i],
            "humidity": humidity[i],
            "wind_speed": windspeed[i]
        })

    return normalized
