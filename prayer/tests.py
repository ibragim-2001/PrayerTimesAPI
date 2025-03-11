import os
from unittest import TestCase
from unittest.mock import patch, MagicMock

from django.http import HttpRequest

from prayer.services.coordinates_service import get_coordinates_by_ip, get_coordinates_by_city

from prayer.services.ip_service import get_user_ip
from prayer.services.translate_service import translate
from prayer.services.prayer_time_service import get_prayers_times


class GetUserIpTestCase(TestCase):

    def test_get_ip_from_x_forwarded_for(self):
        request = HttpRequest()
        request.META['HTTP_X_FORWARDED_FOR'] = '192.168.1.1, 10.0.0.1'
        ip = get_user_ip(request)
        self.assertEqual(ip, '192.168.1.1')

    def test_get_ip_from_remote_addr(self):
        request = HttpRequest()
        request.META['REMOTE_ADDR'] = '10.0.0.1'
        ip = get_user_ip(request)
        self.assertEqual(ip, '10.0.0.1')

    def test_get_ip_only_x_forwarded_for(self):
        request = HttpRequest()
        request.META['HTTP_X_FORWARDED_FOR'] = ''
        request.META['REMOTE_ADDR'] = '172.16.0.1'
        ip = get_user_ip(request)
        self.assertEqual(ip, '172.16.0.1')

    def test_get_ip_no_headers(self):
        request = HttpRequest()
        ip = get_user_ip(request)
        self.assertIsNone(ip)


class TranslateTestCase(TestCase):

    def test_get_translate_success(self):
        translated_word = translate('New-York')
        self.assertEqual(translated_word, 'Нью-Йорк')

    def test_translate_empty_string(self):
        translated_word = translate("")
        self.assertEqual(translated_word, "")

    def test_translate_non_english_word(self):
        translated_word = translate("привет")
        self.assertNotEqual(translated_word, "hello")


class TestGetPrayersTimes(TestCase):

    @patch('requests.get')
    def test_get_prayers_times(self, mock_get):

        os.environ['PRAYER_TIME_API'] = 'http://fakeapi.com'

        mock_response = MagicMock()
        mock_response.json.return_value = {
            "data": {
                "timings": {
                    "Fajr": "05:00",
                    "Sunrise": "06:15",
                    "Dhuhr": "12:30",
                    "Asr": "15:45",
                    "Maghrib": "18:00",
                    "Isha": "19:15"
                },
                "date": {
                    "hijri": {
                        "date": "01-01-1445"
                    }
                }
            }
        }

        mock_get.return_value = mock_response

        today = "2023-10-01"
        latitude = 0.0
        longitude = 0.0
        result = get_prayers_times(today, latitude, longitude)

        expected_result = {
            "Хиджра": "01-01-1445",
            "Фаджр": "05:00",
            "Восход солнца": "06:15",
            "Зухр": "12:30",
            "Аср": "15:45",
            "Магриб": "18:00",
            "Иша": "19:15"
        }

        self.assertEqual(result, expected_result)


class TestCoordinateFunctions(TestCase):

    def test_get_coordinates_by_ip(self):

        user_ip = "63.116.61.253"
        result = get_coordinates_by_ip(user_ip)

        expected = {
            "latitude": 40.7128,
            "longitude": -74.0060,
            "city": "New York"
        }
        self.assertEqual(result, expected)


    def test_get_coordinate_by_city(self):
        result = get_coordinates_by_city('New-York')

        expected = {
            'address': 'City of New York, New York, United States',
            'latitude': 40.7127281,
            'longitude': -74.0060152
        }

        self.assertEqual(result, expected)