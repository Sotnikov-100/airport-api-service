from rest_framework import serializers
from apps.airlines.models import Airline, Aircraft


class AirlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airline
        fields = ("name", "code")


class AircraftSerializer(serializers.ModelSerializer):
    airline = serializers.StringRelatedField()

    class Meta:
        model = Aircraft
        fields = ("model", "airline")
