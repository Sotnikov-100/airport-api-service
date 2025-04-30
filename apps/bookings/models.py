from django.db import models
from apps.core.models import BaseModel
from apps.flights.models import Flight
from apps.users.models import User


class Passenger(BaseModel):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    passport_scan = models.FileField(upload_to="passengers/documents/", null=True)

    class Meta:
        app_label = "bookings"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Booking(BaseModel):
    STATUS_CHOICES = [
        ("confirmed", "Confirmed"),
        ("canceled", "Canceled"),
        ("completed", "Completed"),
    ]

    class Meta:
        app_label = "bookings"

    flight = models.ForeignKey(Flight, on_delete=models.PROTECT)
    passenger = models.ForeignKey(Passenger, on_delete=models.PROTECT)
    seat_number = models.CharField(max_length=10)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="confirmed"
    )
    booked_by = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return f"Booking #{self.id} - {self.passenger} ({self.flight})"
