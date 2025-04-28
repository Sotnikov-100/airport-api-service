from django.db import models

from apps.airlines.models import Aircraft
from apps.core.models import BaseModel


class Country(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=2, unique=True)

    def __str__(self):
        return self.name


class City(BaseModel):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}, {self.country.code}"


class City(BaseModel):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}, {self.country.code}"


class Airport(BaseModel):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=3, unique=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.code} ({self.name})"


class Flight(BaseModel):
    FLIGHT_STATUS_CHOICES = [
        ("scheduled", "Scheduled"),
        ("delayed", "Delayed"),
        ("departed", "Departed"),
        ("arrived", "Arrived"),
        ("canceled", "Canceled"),
    ]

    flight_number = models.CharField(max_length=10, unique=True)
    departure_airport = models.ForeignKey(
        "Airport", on_delete=models.PROTECT, related_name="departing_flights"
    )
    arrival_airport = models.ForeignKey(
        "Airport", on_delete=models.PROTECT, related_name="arriving_flights"
    )
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    aircraft = models.ForeignKey(
        Aircraft, on_delete=models.PROTECT, related_name="flights"
    )
    status = models.CharField(
        max_length=20, choices=FLIGHT_STATUS_CHOICES, default="scheduled"
    )
    available_seats = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["departure_time"]
        indexes = [
            models.Index(fields=["flight_number"]),
            models.Index(fields=["departure_time"]),
            models.Index(fields=["status"]),
        ]

    def __str__(self):
        return (
            f"{self.flight_number}: {self.departure_airport.code} → "
            f"{self.arrival_airport.code} ({self.departure_time:%Y-%m-%d})"
        )

    def duration(self):
        """Calculate flight duration in minutes"""
        if self.arrival_time and self.departure_time:
            return (self.arrival_time - self.departure_time).total_seconds() / 60
        return 0
