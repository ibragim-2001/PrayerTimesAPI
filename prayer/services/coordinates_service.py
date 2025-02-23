import os
import requests
from dotenv.main import rewrite

from geopy.geocoders import Nominatim


def get_coordinates_by_ip(user_ip):
    url = os.getenv("IP_INFO_API_URL")
    response = requests.get(url + user_ip).json()

    return {'latitude': response["lat"], 'longitude': response["lon"], 'city': response["city"]}


def get_coordinates_by_city(user_city):

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