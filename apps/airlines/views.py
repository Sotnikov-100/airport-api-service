from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework import filters
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view

from apps.airlines.models import Airline, Aircraft
from apps.airlines.serializers import AirlineSerializer, AircraftSerializer
from apps.core.pagination import StandardResultsSetPagination
from apps.core.permissions import IsAdminOrReadOnly


@extend_schema_view(
    list=extend_schema(
        summary="List all airlines",
        description="Returns a list of all airlines in the system",
        tags=["Airlines"],
    ),
    retrieve=extend_schema(
        summary="Get an airline by ID",
        description="Returns details of a specific airline",
        tags=["Airlines"],
    ),
    create=extend_schema(
        summary="Create a new airline",
        description="Create a new airline (admin only)",
        tags=["Airlines"],
    ),
    update=extend_schema(
        summary="Update an airline",
        description="Update an existing airline (admin only)",
        tags=["Airlines"],
    ),
    partial_update=extend_schema(
        summary="Partially update an airline",
        description="Partially update an existing airline (admin only)",
        tags=["Airlines"],
    ),
    destroy=extend_schema(
        summary="Delete an airline",
        description="Delete an existing airline (admin only)",
        tags=["Airlines"],
    ),
)
@method_decorator(cache_page(60 * 60), name="list")
@method_decorator(cache_page(60 * 60 * 2), name="retrieve")
class AirlineViewSet(viewsets.ModelViewSet):
    queryset = Airline.objects.all()
    serializer_class = AirlineSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    pagination_class = StandardResultsSetPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    search_fields = ["name", "code"]
    ordering_fields = ["name"]
    ordering = ["name"]


@extend_schema_view(
    list=extend_schema(
        summary="List all aircraft",
        description="Returns a list of all aircraft in the system",
        tags=["Aircraft"],
    ),
    retrieve=extend_schema(
        summary="Get an aircraft by ID",
        description="Returns details of a specific aircraft",
        tags=["Aircraft"],
    ),
    create=extend_schema(
        summary="Create a new aircraft",
        description="Create a new aircraft (admin only)",
        tags=["Aircraft"],
    ),
    update=extend_schema(
        summary="Update an aircraft",
        description="Update an existing aircraft (admin only)",
        tags=["Aircraft"],
    ),
    partial_update=extend_schema(
        summary="Partially update an aircraft",
        description="Partially update an existing aircraft (admin only)",
        tags=["Aircraft"],
    ),
    destroy=extend_schema(
        summary="Delete an aircraft",
        description="Delete an existing aircraft (admin only)",
        tags=["Aircraft"],
    ),
)
@method_decorator(cache_page(60 * 30), name="list")
@method_decorator(cache_page(60 * 60), name="retrieve")
class AircraftViewSet(viewsets.ModelViewSet):
    queryset = Aircraft.objects.select_related("airline")
    serializer_class = AircraftSerializer
    filterset_fields = ["airline"]
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    pagination_class = StandardResultsSetPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    search_fields = ["airline__name", "model"]
    ordering_fields = ["model"]
    ordering = ["model"]
