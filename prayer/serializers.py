from rest_framework import serializers
from .models import Country, Region, City


class CountrySerializer(serializers.ModelSerializer):

    class Meta:
        model = Country
        fields = ("id", "name")


class RegionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Region
        fields = ("id", "name", "country")

class CitySerializer(serializers.ModelSerializer):

    class Meta:
        model = City
        fields = ("id", "name")