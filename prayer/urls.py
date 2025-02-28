from django.urls import path
from prayer.views import *

urlpatterns = [
    path("prayer-time-by-location/", PrayerTimeByLocationView.as_view(), name='prayer-time-by-location'),
    path("city-search/", CitySearchView.as_view(), name="city-search"),
    path("prayer-time-by-city/<int:city_id>/", PrayerTimeByCityView.as_view(), name='prayer-time-by-city')
]