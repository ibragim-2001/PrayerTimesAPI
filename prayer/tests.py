from http import HTTPStatus
from unittest.mock import patch
from geopy.exc import GeocoderUnavailable

from django.urls import reverse
from rest_framework.test import APITestCase

from .models import City, Country, Region


class SearchCityTestCase(APITestCase):

    def setUp(self):
        self.country = Country.objects.create(name='Россия')
        self.region = Region.objects.create(name='Москва и Московская обл.', country=self.country)
        self.city = City.objects.create(name="Москва", region=self.region)

    def test_search_city(self):
        path = reverse('city-search') + '?query=Мос'
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_search_city_not_found(self):
        path = reverse('city-search') + '?query=НеСуществующийГород'
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(response.data, {'message': 'Город не найден'})

    def test_search_city_not_query(self):
        path = reverse('city-search')
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(response.data, {'message': 'Вы ничего не ввели'})

    def tearDown(self):
        pass


class PrayerTimeByCityTestCase(APITestCase):

    def setUp(self):
        """
        Создаем в тестовой базе данных данные
        :return:
        """
        self.country = Country.objects.create(name='Россия')
        self.region = Region.objects.create(name='Москва и Московская обл.', country=self.country)
        self.city = City.objects.create(name="Москва", region=self.region)

    @patch('prayer.services.coordinates_service.get_coordinates_by_city')
    @patch('prayer.services.prayer_time_service.get_prayers_times')
    def test_get_prayer_times_success(self, mock_get_prayers_times=None, mock_get_coordinates=None):
        """
        Этот тест проверяет успешное получение времени молитвы для существующего города.
        Мы используем unittest.mock.patch для замены вызовов к
        внешним сервисам (координаты и время молитвы) на поддельные данные.
        :param mock_get_prayers_times:
        :param mock_get_coordinates:
        :return:
        """
        mock_get_coordinates.return_value = {"latitude": 55.7558, "longitude": 37.6173}

        mock_get_prayers_times.return_value = {
            "fajr": "00:00",
            "dhuhr": "00:00",
            "asr": "00:00",
            "maghrib": "00:00",
            "isha": "00:00"
        }

        path = reverse('prayer-time-by-city', args=[self.city.id])
        response = self.client.get(path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.data['city'], self.city.name)
        self.assertIn('prayer-time', response.data)
        self.assertEqual(response.data['prayer-time'], mock_get_prayers_times.return_value)

    def test_get_prayer_times_city_not_found(self):
        path = reverse('prayer-time-by-city', args=[9999])
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(response.data['error'], 'Город не найден')

    @patch('prayer.services.coordinates_service.get_coordinates_by_city')
    def test_get_prayer_times_coordinates_unavailable(self, mock_get_coordinates):
        # Настраиваем мок для ситуации, когда координаты не найдены
        mock_get_coordinates.return_value = None

        path = reverse('prayer-time-by-city', args=[self.city.id])
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(response.data['error'], 'Не удалось получить координаты города')

    @patch('prayer.services.coordinates_service.get_coordinates_by_city')
    @patch('prayer.services.prayer_time_service.get_prayers_times', side_effect=GeocoderUnavailable)
    def test_get_prayer_times_geocoder_unavailable(self, mock_get_prayers_times, mock_get_coordinates):
        mock_get_coordinates.return_value = {"latitude": 55.7558, "longitude": 37.6173}

        path = reverse('prayer-time-by-city', args=[self.city.id])
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Служба поиска местоположения временно не работает')

    def tearDown(self):
        pass


class PrayerTimeByLocationTestCase(APITestCase):

    def setUp(self):
        self.country = Country.objects.create(name='Россия')
        self.region = Region.objects.create(name='Москва и Московская обл.', country=self.country)
        self.city = City.objects.create(name="Москва", region=self.region)

    @patch('prayer.services.ip_service.get_user_ip')
    @patch('prayer.services.coordinates_service.get_coordinates_by_ip')
    @patch('prayer.services.prayer_time_service.get_prayers_time')
    def get_prayer_time_success(self, mock_get_user_ip, mock_get_coordinates_by_ip,  mock_get_prayers_times):
        mock_get_user_ip.return_value = '111.22.333.444'
        mock_get_coordinates_by_ip.return_value = {"latitude": 00.000, "longitude": 00.000}
        mock_get_prayers_times.return_value = {
            "fajr": "00:00",
            "dhuhr": "00:00",
            "asr": "00:00",
            "maghrib": "00:00",
            "isha": "00:00"
        }

        path = reverse('prayer-time-by-location', args=[self.city.id])
        response = self.client.get(path)
        print(response.status_code)
        # 0 test Не находит тесты??



    def tearDown(self):
        pass