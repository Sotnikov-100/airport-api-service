from django.contrib import admin
from apps.flights.models import Country, City, Airport, Flight


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ("name", "code")
    search_fields = ("name", "code")
    list_per_page = 20


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ("name", "country")
    search_fields = ("name", "country__name")
    list_filter = ("country",)
    raw_id_fields = ("country",)


@admin.register(Airport)
class AirportAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "city")
    search_fields = ("name", "code", "city__name")
    list_filter = ("city__country",)
    raw_id_fields = ("city",)


@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = (
        "flight_number",
        "departure_airport",
        "arrival_airport",
        "departure_time",
        "status",
    )
    search_fields = ("flight_number",)
    list_filter = ("status", "departure_airport__city__country", "aircraft__airline")
    date_hierarchy = "departure_time"
    raw_id_fields = ("departure_airport", "arrival_airport", "aircraft")
    autocomplete_fields = ["departure_airport", "arrival_airport"]
