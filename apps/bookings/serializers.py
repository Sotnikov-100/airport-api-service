from rest_framework import serializers
from apps.bookings.models import Passenger, Booking
from apps.flights.models import Flight
from apps.flights.serializers import FlightSerializer


class PassengerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Passenger
        fields = ("first_name", "last_name", "email")


class BookingSerializer(serializers.ModelSerializer):
    flight = FlightSerializer(read_only=True)
    passenger = PassengerSerializer(read_only=True)
    flight_id = serializers.PrimaryKeyRelatedField(
        queryset=Flight.objects.all(), write_only=True, source="flight"
    )
    passenger_id = serializers.PrimaryKeyRelatedField(
        queryset=Passenger.objects.all(), write_only=True, source="passenger"
    )

    class Meta:
        model = Booking
        fields = (
            "id",
            "flight",
            "passenger",
            "seat_number",
            "status",
            "booked_by",
            "flight_id",
            "passenger_id",
        )
        read_only_fields = ["booked_by", "status"]
