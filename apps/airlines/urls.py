from rest_framework.routers import DefaultRouter
from .views import (
    AirlineViewSet,
    AircraftViewSet,
)


router = DefaultRouter()
router.register(r"airlines", AirlineViewSet, basename="airlines")
router.register(r"aircrafts", AircraftViewSet, basename="aircrafts")

urlpatterns = router.urls

app_name = "airlines"
