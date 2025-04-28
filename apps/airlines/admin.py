from django.contrib import admin
from apps.airlines.models import Airline, Aircraft


@admin.register(Airline)
class AirlineAdmin(admin.ModelAdmin):
    list_display = ("name", "code")
    search_fields = ("name", "code")


@admin.register(Aircraft)
class AircraftAdmin(admin.ModelAdmin):
    list_display = ("model", "airline")
    list_filter = ("airline",)
    search_fields = ("model",)
