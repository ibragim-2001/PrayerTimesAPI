from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import City
from .serializers import CitySerializer

from .utils.time_utils import TODAY_DATE

from .services import (
    ip_service,
    coordinates_service,
    prayer_time_service,
)


class PrayerTimeByLocationView(APIView):

    def get(self, request):
        user_ip = ip_service.get_user_ip(request)

        if user_ip == '127.0.0.1' or user_ip is None:
            return Response({'message': 'Не удалось определить ваше местоположение'},status.HTTP_400_BAD_REQUEST)

        coordinates = coordinates_service.get_coordinates_by_ip(user_ip)
        prayer_time = prayer_time_service.get_prayers_times(
            TODAY_DATE,
            coordinates['latitude'],
            coordinates['longitude']
        )

        return Response(data={'city': coordinates['city'], 'prayer-time': prayer_time}, status=status.HTTP_200_OK)


class CitySearchView(APIView):

    def get(self, request):
        query = request.GET.get('query', None)

        if not query:
            return Response(data={'message':'Вы ничего не ввели'}, status=status.HTTP_400_BAD_REQUEST)

        cities = City.objects.filter(name__icontains=query)
        serializer = CitySerializer(cities, many=True)

        if not cities.exists():
            return Response({'message': 'Город не найден'}, status=status.HTTP_404_NOT_FOUND)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class PrayerTimeByCityView(APIView):

    def get(self, request, city_id):
        try:
            user_city = City.objects.get(id=city_id)
            coordinates = coordinates_service.get_coordinates_by_city(user_city=user_city)
            prayer_time = prayer_time_service.get_prayers_times(
                TODAY_DATE,
                coordinates['latitude'],
                coordinates['longitude']
            )
            return Response(data={'city': user_city.name, 'prayer-time': prayer_time}, status=status.HTTP_200_OK)
        except City.DoesNotExist:
            return Response({'error': 'Город не найден'}, status=status.HTTP_404_NOT_FOUND)