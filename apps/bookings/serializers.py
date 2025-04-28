from rest_framework import serializers
from apps.bookings.models import Passenger, Booking


class PassengerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Passenger
        fields = ("first_name", "last_name", "email")


class BookingSerializer(serializers.ModelSerializer):
    flight = serializers.StringRelatedField()
    passenger = serializers.StringRelatedField()

    class Meta:
        model = Booking
        fields = ("flight", "passenger", "seat_number", "status", "booked_by")
        read_only_fields = ["booked_by", "status"]
