import requests

from ingestion.database import RawWeather, save_raw_record

CITIES = [
    ("New York", 40.7128, -74.0060),
    ("Los Angeles", 34.0522, -118.2437),
    ("Chicago", 41.8781, -87.6298),
    ("Houston", 29.7604, -95.3698),
    ("Miami", 25.7617, -80.1918),
    ("Phoenix", 33.4484, -112.0740),
    ("Philadelphia", 39.9526, -75.1652),
    ("Dallas", 32.7767, -96.7970),
    ("Atlanta", 33.7490, -84.3880),
    ("Washington, DC", 38.9072, -77.0369),
]

BASE_URL = "https://api.open-meteo.com/v1/forecast"


def ingest_weather(session):
    inserted = 0
    for city_name, latitude, longitude in CITIES:
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "current_weather": "true",
            "timezone": "America/New_York",
        }
        response = requests.get(BASE_URL, params=params, timeout=15)
        response.raise_for_status()
        payload = response.json()
        payload["requested_city"] = city_name
        payload["requested_latitude"] = latitude
        payload["requested_longitude"] = longitude

        save_raw_record(session, RawWeather, "open-meteo", payload)
        inserted += 1
    session.commit()
    return inserted
