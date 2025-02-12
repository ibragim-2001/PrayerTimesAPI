from rest_framework.views import APIView
from rest_framework.response import Response

from .utils.time_utils import TODAY_DATE

from .services import (
    ip_service,
    coordinates_service,
    prayer_time_service
)


class PrayerTimeByLocationView(APIView):

    def get(self, request):
        user_ip = ip_service.get_user_ip(request)
        coordinates = coordinates_service.get_coordinates(user_ip)
        prayer_time = prayer_time_service.get_prayers_times(TODAY_DATE, coordinates["lat"], coordinates["lon"])
        return Response({"ip": user_ip, "coordinates": coordinates, "prayer-time": prayer_time})

