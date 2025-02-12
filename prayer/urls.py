from django.urls import path
from prayer.views import *

urlpatterns = [
    path("prayer-time-by-location/", PrayerTimeByLocationView.as_view()),
]