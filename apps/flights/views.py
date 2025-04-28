from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
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
        "departure_airport", "arrival_airport", "aircraft"
    )
    serializer_class = FlightSerializer
    filterset_fields = ["status", "departure_airport", "arrival_airport"]

    @action(detail=True, methods=["get"])
    def available_seats(self, request, pk=None):
        flight = self.get_object()
        return Response(
            {"flight": flight.flight_number, "available_seats": flight.available_seats}
        )

    def get_serializer_class(self):
        if self.action == "retrieve":
            return FlightDetailSerializer
        return super().get_serializer_class()
