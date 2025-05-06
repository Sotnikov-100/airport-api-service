from rest_framework import viewsets, filters, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from django.db.models import Q, Count
from datetime import datetime
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiParameter,
    OpenApiExample,
    OpenApiResponse,
)

from apps.core.pagination import StandardResultsSetPagination
from apps.core.permissions import IsAdminOrReadOnly
from apps.flights.models import Country, City, Airport, Flight
from apps.flights.serializers import (
    CountrySerializer,
    CitySerializer,
    AirportSerializer,
    FlightSerializer,
    FlightDetailSerializer,
)


@extend_schema_view(
    list=extend_schema(
        summary="List all countries",
        description="Returns a list of all countries in the system",
        tags=["Countries"],
    ),
    retrieve=extend_schema(
        summary="Get a country by ID",
        description="Returns details of a specific country",
        tags=["Countries"],
    ),
    create=extend_schema(
        summary="Create a new country",
        description="Create a new country (admin only)",
        tags=["Countries"],
    ),
    update=extend_schema(
        summary="Update a country",
        description="Update an existing country (admin only)",
        tags=["Countries"],
    ),
    partial_update=extend_schema(
        summary="Partially update a country",
        description="Partially update an existing country (admin only)",
        tags=["Countries"],
    ),
    destroy=extend_schema(
        summary="Delete a country",
        description="Delete an existing country (admin only)",
        tags=["Countries"],
    ),
)
@method_decorator(cache_page(60 * 60), name="list")
@method_decorator(cache_page(60 * 60 * 2), name="retrieve")
class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = [IsAdminOrReadOnly]


@extend_schema_view(
    list=extend_schema(
        summary="List all cities",
        description="Returns a list of all cities in the system",
        tags=["Cities"],
    ),
    retrieve=extend_schema(
        summary="Get a city by ID",
        description="Returns details of a specific city",
        tags=["Cities"],
    ),
    create=extend_schema(
        summary="Create a new city",
        description="Create a new city (admin only)",
        tags=["Cities"],
    ),
    update=extend_schema(
        summary="Update a city",
        description="Update an existing city (admin only)",
        tags=["Cities"],
    ),
    partial_update=extend_schema(
        summary="Partially update a city",
        description="Partially update an existing city (admin only)",
        tags=["Cities"],
    ),
    destroy=extend_schema(
        summary="Delete a city",
        description="Delete an existing city (admin only)",
        tags=["Cities"],
    ),
)
@method_decorator(cache_page(60 * 60), name="list")
@method_decorator(cache_page(60 * 60 * 2), name="retrieve")
class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.select_related("country")
    serializer_class = CitySerializer
    permission_classes = [IsAdminOrReadOnly]


@extend_schema_view(
    list=extend_schema(
        summary="List all airports",
        description="Returns a list of all airports in the system",
        tags=["Airports"],
    ),
    retrieve=extend_schema(
        summary="Get an airport by ID",
        description="Returns details of a specific airport",
        tags=["Airports"],
    ),
    create=extend_schema(
        summary="Create a new airport",
        description="Create a new airport (admin only)",
        tags=["Airports"],
    ),
    update=extend_schema(
        summary="Update an airport",
        description="Update an existing airport (admin only)",
        tags=["Airports"],
    ),
    partial_update=extend_schema(
        summary="Partially update an airport",
        description="Partially update an existing airport (admin only)",
        tags=["Airports"],
    ),
    destroy=extend_schema(
        summary="Delete an airport",
        description="Delete an existing airport (admin only)",
        tags=["Airports"],
    ),
)
@method_decorator(cache_page(60 * 15), name="list")
@method_decorator(cache_page(60 * 30), name="retrieve")
class AirportViewSet(viewsets.ModelViewSet):
    queryset = Airport.objects.select_related("city")
    serializer_class = AirportSerializer
    permission_classes = [IsAdminOrReadOnly]


@extend_schema_view(
    list=extend_schema(
        summary="List all flights",
        description="Returns a list of all flights in the system",
        tags=["Flights"],
    ),
    retrieve=extend_schema(
        summary="Get a flight by ID",
        description="Returns detailed information about a specific flight",
        tags=["Flights"],
    ),
    create=extend_schema(
        summary="Create a new flight",
        description="Create a new flight (admin only)",
        tags=["Flights"],
    ),
    update=extend_schema(
        summary="Update a flight",
        description="Update an existing flight (admin only)",
        tags=["Flights"],
    ),
    partial_update=extend_schema(
        summary="Partially update a flight",
        description="Partially update an existing flight (admin only)",
        tags=["Flights"],
    ),
    destroy=extend_schema(
        summary="Delete a flight",
        description="Delete an existing flight (admin only)",
        tags=["Flights"],
    ),
)
@method_decorator(cache_page(60 * 5), name="list")
@method_decorator(vary_on_cookie, name="list")
@method_decorator(cache_page(60 * 10), name="retrieve")
@method_decorator(vary_on_cookie, name="retrieve")
class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.select_related(
        "departure_airport", "arrival_airport", "aircraft", "aircraft__airline"
    )
    serializer_class = FlightSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    pagination_class = StandardResultsSetPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = {
        "status": ["exact"],
        "departure_airport": ["exact"],
        "arrival_airport": ["exact"],
        "departure_time": ["gte", "lte", "date"],
        "arrival_time": ["gte", "lte", "date"],
        "aircraft__airline": ["exact"],
        "available_seats": ["gte"],
    }
    search_fields = [
        "flight_number",
        "departure_airport__code",
        "arrival_airport__code",
    ]
    ordering_fields = ["departure_time", "arrival_time", "available_seats"]
    ordering = ["departure_time"]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return FlightDetailSerializer
        return super().get_serializer_class()

    @extend_schema(
        summary="Get available seats",
        description="Returns the number of available seats for a specific flight",
        responses={200: OpenApiResponse(description="Number of available seats")},
        tags=["Flights"],
    )
    @method_decorator(cache_page(60 * 5))
    @action(detail=True, methods=["get"])
    def available_seats(self, request, pk=None):
        flight = self.get_object()
        return Response(
            {"flight": flight.flight_number, "available_seats": flight.available_seats}
        )

    @extend_schema(
        summary="Search flights",
        description="Search flights with from-to airport codes and optional date",
        parameters=[
            OpenApiParameter(
                name="from",
                description="Departure airport code",
                required=True,
                type=str,
                location=OpenApiParameter.QUERY,
            ),
            OpenApiParameter(
                name="to",
                description="Arrival airport code",
                required=True,
                type=str,
                location=OpenApiParameter.QUERY,
            ),
            OpenApiParameter(
                name="date",
                description="Departure date (YYYY-MM-DD)",
                required=False,
                type=str,
                location=OpenApiParameter.QUERY,
            ),
        ],
        responses={
            200: FlightSerializer(many=True),
            400: OpenApiResponse(description="Bad request - invalid parameters"),
        },
        tags=["Flights"],
    )
    @action(detail=False, methods=["get"])
    def search(self, request):
        """
        Search flights with from-to and date parameters
        """
        from_code = request.query_params.get("from")
        to_code = request.query_params.get("to")
        date_str = request.query_params.get("date")

        if not from_code or not to_code:
            return Response(
                {"error": "Both 'from' and 'to' parameters are required"}, status=400
            )

        query = Q(departure_airport__code=from_code) & Q(arrival_airport__code=to_code)

        if date_str:
            try:
                date = datetime.strptime(date_str, "%Y-%m-%d").date()
                query &= Q(departure_time__date=date)
            except ValueError:
                return Response(
                    {"error": "Invalid date format. Use YYYY-MM-DD"}, status=400
                )

        flights = self.get_queryset().filter(query)
        serializer = self.get_serializer(flights, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Get flight statistics",
        description="Returns statistics about flights grouped by status",
        responses={
            200: OpenApiResponse(
                description="Flight statistics",
                examples=[
                    OpenApiExample(
                        "Example response",
                        value=[
                            {"status": "scheduled", "count": 42},
                            {"status": "delayed", "count": 7},
                            {"status": "in_air", "count": 12},
                            {"status": "landed", "count": 30},
                            {"status": "cancelled", "count": 3},
                        ],
                    )
                ],
            )
        },
        tags=["Flights"],
    )
    @action(detail=False, methods=["get"])
    def statistics(self, request):
        stats = Flight.objects.values("status").annotate(count=Count("status"))
        return Response(stats)

    @extend_schema(
        summary="Get upcoming flights",
        description="Returns a list of upcoming scheduled flights within the next 24 hours",
        responses={200: FlightSerializer(many=True)},
        tags=["Flights"],
    )
    @action(detail=False, methods=["get"])
    def upcoming(self, request):
        now = timezone.now()
        tomorrow = now + timezone.timedelta(days=1)
        flights = self.get_queryset().filter(
            departure_time__gte=now, departure_time__lte=tomorrow, status="scheduled"
        )
        page = self.paginate_queryset(flights)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(flights, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Update flight status",
        description="Update the status of a specific flight (admin only)",
        request={
            "application/json": {
                "type": "object",
                "properties": {
                    "status": {
                        "type": "string",
                        "enum": [
                            "scheduled",
                            "delayed",
                            "in_air",
                            "landed",
                            "cancelled",
                        ],
                    }
                },
                "required": ["status"],
            }
        },
        responses={
            200: FlightSerializer,
            400: OpenApiResponse(description="Invalid status value"),
        },
        tags=["Flights"],
    )
    @action(detail=True, methods=["post"])
    def update_status(self, request, pk=None):
        flight = self.get_object()
        new_status = request.data.get("status")
        if not new_status or new_status not in dict(Flight.FLIGHT_STATUS_CHOICES):
            return Response(
                {"error": "Invalid or missing status"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        flight.status = new_status
        flight.save()
        serializer = self.get_serializer(flight)
        return Response(serializer.data)
