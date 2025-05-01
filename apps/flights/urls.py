from rest_framework.routers import DefaultRouter
from apps.flights.views import (
    CountryViewSet,
    CityViewSet,
    AirportViewSet,
    FlightViewSet,
)

router = DefaultRouter()
router.register(r"countries", CountryViewSet)
router.register(r"cities", CityViewSet)
router.register(r"airports", AirportViewSet)
router.register(r"flights", FlightViewSet)

urlpatterns = router.urls

app_name = "flights"
