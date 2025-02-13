import os
import requests


def get_coordinates(user_ip):
    url = os.getenv("IP_INFO_API_URL")
    response = requests.get(url + user_ip).json()

    return {'latitude': response["lat"], 'longitude': response["lon"], 'city': response["city"]}