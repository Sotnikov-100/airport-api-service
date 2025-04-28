from rest_framework.routers import DefaultRouter
from .views import (
    AirlineViewSet,
    AircraftViewSet,
)


router = DefaultRouter()
router.register(r"airlines", AirlineViewSet)
router.register(r"aircrafts", AircraftViewSet)

urlpatterns = router.urls
