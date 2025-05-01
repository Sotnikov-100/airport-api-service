from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated

from apps.core.pagination import StandardResultsSetPagination
from apps.core.permissions import IsOwnerOrAdmin
from apps.bookings.models import Passenger, Booking
from apps.bookings.serializers import PassengerSerializer, BookingSerializer


class PassengerViewSet(viewsets.ModelViewSet):
    queryset = Passenger.objects.all()
    serializer_class = PassengerSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["first_name", "last_name", "email"]
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


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    pagination_class = StandardResultsSetPagination
    filterset_fields = ["status", "flight"]
    search_fields = [
        "passenger__first_name",
        "passenger__last_name",
        "flight__flight_number",
    ]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Booking.objects.all().select_related(
                "flight", "passenger", "booked_by"
            )
        return Booking.objects.filter(booked_by=user).select_related(
            "flight", "passenger"
        )

    def perform_create(self, serializer):
        serializer.save(booked_by=self.request.user)

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    search_fields = [
        "passenger__first_name",
        "passenger__last_name",
        "flight__flight_number",
    ]
    ordering_fields = ["status", "flight"]
    ordering = ["status"]
