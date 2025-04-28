from rest_framework import viewsets
from apps.bookings.models import Passenger, Booking
from apps.bookings.serializers import PassengerSerializer, BookingSerializer
from rest_framework.permissions import IsAuthenticated


class PassengerViewSet(viewsets.ModelViewSet):
    queryset = Passenger.objects.all()
    serializer_class = PassengerSerializer
    search_fields = ["first_name", "last_name", "email"]


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(booked_by=self.request.user).select_related(
            "flight", "passenger"
        )

    def perform_create(self, serializer):
        serializer.save(booked_by=self.request.user)
