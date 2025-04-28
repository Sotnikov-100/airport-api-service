from rest_framework import serializers

from apps.airlines.serializers import AircraftSerializer
from apps.flights.models import Country, City, Airport, Flight


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ("code", "name")


class CitySerializer(serializers.ModelSerializer):
    country = serializers.StringRelatedField()

    class Meta:
        model = City
        fields = ("name", "country")


class AirportSerializer(serializers.ModelSerializer):
    city = serializers.StringRelatedField()

    class Meta:
        model = Airport
        fields = ("name", "code", "city")


class FlightSerializer(serializers.ModelSerializer):
    departure_airport = serializers.StringRelatedField()
    arrival_airport = serializers.StringRelatedField()
    aircraft = serializers.StringRelatedField()

    class Meta:
        model = Flight
        fields = (
            "flight_number",
            "departure_airport",
            "arrival_airport",
            "departure_time",
            "arrival_time",
            "aircraft",
            "status",
            "available_seats",
        )


class FlightDetailSerializer(serializers.ModelSerializer):
    departure_airport = serializers.StringRelatedField()
    arrival_airport = serializers.StringRelatedField()
    aircraft = AircraftSerializer()

    class Meta:
        model = Flight
        fields = ("flight_number", "departure_airport", "arrival_airport", "aircraft")
