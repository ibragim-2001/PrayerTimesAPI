import requests

def get_coordinates(user_ip):
    url = 'http://ip-api.com/json/'
    response = requests.get(url + user_ip).json()
    lat = response["lat"]
    lon = response["lon"]

    return {'lat': lat, 'lon': lon}

# Спрятать URL