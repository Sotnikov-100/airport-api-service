from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema_view

from apps.core.pagination import StandardResultsSetPagination
from apps.core.permissions import IsOwnerOrAdmin
from apps.bookings.models import Passenger, Booking
from apps.bookings.serializers import PassengerSerializer, BookingSerializer
from apps.bookings.schemas import passenger_schemas, booking_schemas


@extend_schema_view(**passenger_schemas)
class PassengerViewSet(viewsets.ModelViewSet):
    queryset = Passenger.objects.all()
    serializer_class = PassengerSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    search_fields = ["first_name", "last_name", "email"]
    ordering_fields = ["first_name", "last_name"]
    ordering = ["first_name"]


@extend_schema_view(**booking_schemas)
class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
    pagination_class = StandardResultsSetPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["status", "flight"]
    search_fields = [
        "passenger__first_name",
        "passenger__last_name",
        "flight__flight_number",
    ]
    ordering_fields = ["status", "flight"]
    ordering = ["status"]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Booking.objects.select_related("flight", "passenger", "booked_by")
        return Booking.objects.filter(booked_by=user).select_related(
            "flight", "passenger"
        )

    def perform_create(self, serializer):
        serializer.save(booked_by=self.request.user)
