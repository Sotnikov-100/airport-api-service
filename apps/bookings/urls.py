from rest_framework.routers import DefaultRouter
from apps.bookings.views import (
    PassengerViewSet,
    BookingViewSet,
)


router = DefaultRouter()
router.register(r"passengers", PassengerViewSet)
router.register(r"bookings", BookingViewSet)

urlpatterns = router.urls
