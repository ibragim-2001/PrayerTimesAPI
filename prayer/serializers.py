from rest_framework import serializers
from .models import Country, Region, City


class CountrySerializer(serializers.ModelSerializer):

    class Meta:
        model = Country
        fields = ("name", )


class RegionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Region
        fields = ("name", "country")

class CitySerializer(serializers.ModelSerializer):
    region = serializers.CharField(source="region.name")
    country = serializers.CharField(source="region.country.name")

    class Meta:
        model = City
        fields = ("country", "region", "name", "id")