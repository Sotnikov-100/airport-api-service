from rest_framework.routers import DefaultRouter
from apps.bookings.views import (
    PassengerViewSet,
    BookingViewSet,
)


router = DefaultRouter()
router.register(r"passengers", PassengerViewSet, basename="passenger")
router.register(r"bookings", BookingViewSet, basename="booking")

urlpatterns = router.urls

app_name = "bookings"
