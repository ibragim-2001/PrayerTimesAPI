from django.urls import path
from prayer.views import *

urlpatterns = [
    path('get-ip/', GetIpAPI.as_view())
]