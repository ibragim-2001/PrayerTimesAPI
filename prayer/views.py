from typing import Dict, Optional

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.http import HttpRequest, HttpResponse

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from geopy.exc import GeocoderUnavailable

from .models import City
from .serializers import CitySerializer

from .utils.time_utils import TODAY_DATE

from .services import (
    ip_service,
    coordinates_service,
    prayer_time_service,
    translate_service
)


class PrayerTimeByLocationView(APIView):

    def get(self, request: HttpRequest) -> HttpResponse:
        user_ip: Optional[str] = ip_service.get_user_ip(request)

        if user_ip == "127.0.0.1" or user_ip is None:
            return Response(data={"message": "Не удалось определить ваше местоположение"}, status=status.HTTP_400_BAD_REQUEST)

        coordinates: Dict[str, float] = coordinates_service.get_coordinates_by_ip(user_ip)

        if not coordinates:
            return Response(data={"message": "Не удалось получить координаты по IP"}, status=status.HTTP_404_NOT_FOUND)

        prayer_time: Dict[str, str] = prayer_time_service.get_prayers_times(
            TODAY_DATE,
            coordinates["latitude"],
            coordinates["longitude"]
        )

        return Response(data={"city": translate_service.translate(str(coordinates["city"])), "prayer-time": prayer_time}, status=status.HTTP_200_OK)


class CitySearchView(APIView):

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "query",
                openapi.IN_QUERY,
                description="Параметр запроса",
                type=openapi.TYPE_STRING)
        ]
    )

    def get(self, request: HttpRequest) -> HttpResponse:
        query: Optional[str] = request.GET.get("query", None)

        if not query:
            return Response(data={"message":"Вы ничего не ввели"}, status=status.HTTP_400_BAD_REQUEST)

        cities = City.objects.filter(name__icontains=query)

        if not cities.exists():
            return Response(data={"message": "Город не найден"}, status=status.HTTP_404_NOT_FOUND)

        serializer: CitySerializer = CitySerializer(cities, many=True)

        if not cities.exists():
            return Response(data={"message": "Город не найден"}, status=status.HTTP_404_NOT_FOUND)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class PrayerTimeByCityView(APIView):

    def get(self, request: HttpRequest, city_id: int) -> HttpResponse:
        try:
            user_city = City.objects.get(id=city_id)
            coordinates: Dict[str, float] = coordinates_service.get_coordinates_by_city(user_city=user_city)

            if not coordinates:
                return Response({"error": "Не удалось получить координаты города"}, status=status.HTTP_404_NOT_FOUND)

            prayer_time: Dict[str, str] = prayer_time_service.get_prayers_times(
                TODAY_DATE,
                coordinates["latitude"],
                coordinates["longitude"]
            )

            return Response(data={"city": user_city.name,"prayer-time": prayer_time},status=status.HTTP_200_OK)
        except City.DoesNotExist:
            return Response(data={"error": "Город не найден"},status=status.HTTP_404_NOT_FOUND)
        except GeocoderUnavailable:
            return Response(data={"error": "Служба поиска местоположения временно не работает"}, status=status.HTTP_400_BAD_REQUEST)