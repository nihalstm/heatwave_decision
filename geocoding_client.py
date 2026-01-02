import requests

NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"


def geocode_location(location: str):
    """
    Convert a human-readable location name into latitude and longitude
    using OpenStreetMap Nominatim.

    Returns:
        dict with keys: latitude, longitude, display_name
        or None if location not found
    """

    params = {
        "q": location,
        "format": "json",
        "limit": 1
    }

    headers = {
        "User-Agent": "Heatwave-Decision-Support/1.0"
    }

    try:
        response = requests.get(
            NOMINATIM_URL,
            params=params,
            headers=headers,
            timeout=10
        )
        response.raise_for_status()
    except requests.RequestException:
        return None

    data = response.json()

    if not data:
        return None

    return {
        "latitude": float(data[0]["lat"]),
        "longitude": float(data[0]["lon"]),
        "display_name": data[0]["display_name"]
    }
