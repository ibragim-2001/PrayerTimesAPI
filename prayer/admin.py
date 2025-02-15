from django.contrib import admin
from .models import *


class CityInline(admin.StackedInline):
    model = City


class RegionInline(admin.StackedInline):
    model = Region


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    inlines = [RegionInline]
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    inlines = [CityInline]
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name", )