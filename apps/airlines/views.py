from rest_framework import viewsets
from apps.airlines.models import Airline, Aircraft
from apps.airlines.serializers import AirlineSerializer, AircraftSerializer
from apps.core.permissions import IsAdminOrReadOnly


class AirlineViewSet(viewsets.ModelViewSet):
    queryset = Airline.objects.all()
    serializer_class = AirlineSerializer
    search_fields = ["name", "code"]
    permission_classes = [IsAdminOrReadOnly]


class AircraftViewSet(viewsets.ModelViewSet):
    queryset = Aircraft.objects.select_related("airline")
    serializer_class = AircraftSerializer
    filterset_fields = ["airline"]
    permission_classes = [IsAdminOrReadOnly]
