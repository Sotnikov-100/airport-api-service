from rest_framework import serializers

from apps.airlines.serializers import AircraftSerializer
from apps.flights.models import Country, City, Airport, Flight


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ("code", "name")


class CitySerializer(serializers.ModelSerializer):
    country = serializers.PrimaryKeyRelatedField(queryset=Country.objects.all())

    class Meta:
        model = City
        fields = ("name", "country")
        extra_kwargs = {"country": {"required": True}}


class AirportSerializer(serializers.ModelSerializer):
    city = serializers.PrimaryKeyRelatedField(queryset=City.objects.all())

    class Meta:
        model = Airport
        fields = ("name", "code", "city")
        extra_kwargs = {"city": {"required": True}}


class FlightSerializer(serializers.ModelSerializer):
    departure_airport = AirportSerializer()
    arrival_airport = AirportSerializer()
    aircraft = AircraftSerializer()
    duration_minutes = serializers.SerializerMethodField()

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
            "duration_minutes",
        )

    def get_duration_minutes(self, obj):
        return obj.duration()


class FlightDetailSerializer(serializers.ModelSerializer):
    departure_airport = serializers.StringRelatedField()
    arrival_airport = serializers.StringRelatedField()
    aircraft = AircraftSerializer()

    class Meta:
        model = Flight
        fields = ("flight_number", "departure_airport", "arrival_airport", "aircraft")
