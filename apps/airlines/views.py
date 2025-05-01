from rest_framework import viewsets
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from apps.airlines.models import Airline, Aircraft
from apps.airlines.serializers import AirlineSerializer, AircraftSerializer
from apps.core.permissions import IsAdminOrReadOnly


@method_decorator(cache_page(60 * 60), name="list")
@method_decorator(cache_page(60 * 60 * 2), name="retrieve")
class AirlineViewSet(viewsets.ModelViewSet):
    queryset = Airline.objects.all()
    serializer_class = AirlineSerializer
    search_fields = ["name", "code"]
    permission_classes = [IsAdminOrReadOnly]


@method_decorator(cache_page(60 * 30), name="list")
@method_decorator(cache_page(60 * 60), name="retrieve")
class AircraftViewSet(viewsets.ModelViewSet):
    queryset = Aircraft.objects.select_related("airline")
    serializer_class = AircraftSerializer
    filterset_fields = ["airline"]
    permission_classes = [IsAdminOrReadOnly]
