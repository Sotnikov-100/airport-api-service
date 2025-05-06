from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view

from apps.core.pagination import StandardResultsSetPagination
from apps.core.permissions import IsOwnerOrAdmin
from apps.bookings.models import Passenger, Booking
from apps.bookings.serializers import PassengerSerializer, BookingSerializer


@extend_schema_view(
    list=extend_schema(
        summary="List all passengers",
        description="Returns a list of all passengers accessible to the authenticated user",
        tags=["Passengers"],
    ),
    retrieve=extend_schema(
        summary="Get a passenger by ID",
        description="Returns details of a specific passenger",
        tags=["Passengers"],
    ),
    create=extend_schema(
        summary="Create a new passenger",
        description="Create a new passenger record",
        tags=["Passengers"],
    ),
    update=extend_schema(
        summary="Update a passenger",
        description="Update an existing passenger record",
        tags=["Passengers"],
    ),
    partial_update=extend_schema(
        summary="Partially update a passenger",
        description="Partially update an existing passenger record",
        tags=["Passengers"],
    ),
    destroy=extend_schema(
        summary="Delete a passenger",
        description="Delete an existing passenger record",
        tags=["Passengers"],
    ),
)
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


@extend_schema_view(
    list=extend_schema(
        summary="List all bookings",
        description="Returns a list of all bookings accessible to the authenticated user. Regular users see only their own bookings, staff see all bookings.",
        tags=["Bookings"],
    ),
    retrieve=extend_schema(
        summary="Get a booking by ID",
        description="Returns details of a specific booking if accessible to the user",
        tags=["Bookings"],
    ),
    create=extend_schema(
        summary="Create a new booking",
        description="Create a new booking. The current user will be set as the booking owner.",
        tags=["Bookings"],
    ),
    update=extend_schema(
        summary="Update a booking",
        description="Update an existing booking if the user is the owner or admin",
        tags=["Bookings"],
    ),
    partial_update=extend_schema(
        summary="Partially update a booking",
        description="Partially update an existing booking if the user is the owner or admin",
        tags=["Bookings"],
    ),
    destroy=extend_schema(
        summary="Delete a booking",
        description="Delete an existing booking if the user is the owner or admin",
        tags=["Bookings"],
    ),
)
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
