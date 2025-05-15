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
from drf_spectacular.utils import extend_schema_view

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
from apps.flights.schemas import (
    country_schemas,
    city_schemas,
    airport_schemas,
    flight_schemas,
    flight_action_schemas,
)


@extend_schema_view(**country_schemas)
@method_decorator(cache_page(60 * 60), name="list")
@method_decorator(cache_page(60 * 60 * 2), name="retrieve")
class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = [IsAdminOrReadOnly]


@extend_schema_view(**city_schemas)
@method_decorator(cache_page(60 * 60), name="list")
@method_decorator(cache_page(60 * 60 * 2), name="retrieve")
class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.select_related("country")
    serializer_class = CitySerializer
    permission_classes = [IsAdminOrReadOnly]


@extend_schema_view(**airport_schemas)
@method_decorator(cache_page(60 * 15), name="list")
@method_decorator(cache_page(60 * 30), name="retrieve")
class AirportViewSet(viewsets.ModelViewSet):
    queryset = Airport.objects.select_related("city")
    serializer_class = AirportSerializer
    permission_classes = [IsAdminOrReadOnly]


@extend_schema_view(**flight_schemas)
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

    @flight_action_schemas["available_seats"]
    @method_decorator(cache_page(60 * 5))
    @action(detail=True, methods=["get"])
    def available_seats(self, request, pk=None):
        flight = self.get_object()
        return Response(
            {"flight": flight.flight_number, "available_seats": flight.available_seats}
        )

    @flight_action_schemas["search"]
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

    @flight_action_schemas["statistics"]
    @action(detail=False, methods=["get"])
    def statistics(self, request):
        stats = Flight.objects.values("status").annotate(count=Count("status"))
        return Response(stats)

    @flight_action_schemas["upcoming"]
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

    @flight_action_schemas["update_status"]
    @action(detail=True, methods=["post"])
    def update_status(self, request, pk=None):
        flight = self.get_object()
        new_status = request.data.get("status")
        if not new_status or new_status not in Flight.StatusChoices.values:
            return Response(
                {"error": "Invalid or missing status"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        flight.status = new_status
        flight.save()
        serializer = self.get_serializer(flight)
        return Response(serializer.data)
