import os
import requests
from typing import Dict, Union

from geopy.geocoders import Nominatim


def get_coordinates_by_ip(user_ip: str):
    url: str = os.getenv("IP_INFO_API_URL")
    response: Dict[str, Union[str, float]] = requests.get(url + user_ip).json()

    return {"latitude": response["lat"], "longitude": response["lon"], "city": response["city"]}


def get_coordinates_by_city(user_city: str):

    geolocator = Nominatim(user_agent="MyGeocoder")
    location = geolocator.geocode(user_city)

    if location is not None:
        return {
            "address": location.address,
            "latitude": location.latitude,  # Широта
            "longitude": location.longitude  # Долгота
        }
    else:
        return None