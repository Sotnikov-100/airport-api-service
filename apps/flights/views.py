from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from datetime import datetime
from apps.flights.models import Country, City, Airport, Flight
from apps.flights.serializers import (
    CountrySerializer,
    CitySerializer,
    AirportSerializer,
    FlightSerializer,
    FlightDetailSerializer,
)


class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.select_related("country")
    serializer_class = CitySerializer


class AirportViewSet(viewsets.ModelViewSet):
    queryset = Airport.objects.select_related("city")
    serializer_class = AirportSerializer


class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.select_related(
        "departure_airport", "arrival_airport", "aircraft", "aircraft__airline"
    )
    serializer_class = FlightSerializer
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

    @action(detail=True, methods=["get"])
    def available_seats(self, request, pk=None):
        flight = self.get_object()
        return Response(
            {"flight": flight.flight_number, "available_seats": flight.available_seats}
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

    def get_serializer_class(self):
        if self.action == "retrieve":
            return FlightDetailSerializer
        return super().get_serializer_class()
