from django.urls import path
from prayer.views import *

urlpatterns = [
    path("prayer-time-by-location/", PrayerTimeByLocationView.as_view()),
    path("city-search/", CitySearchView.as_view()),
    path("prayer-time-by-city/<int:city_id>/", PrayerTimeByCityView.as_view())
]