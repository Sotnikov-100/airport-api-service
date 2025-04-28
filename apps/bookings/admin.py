from django.contrib import admin
from apps.bookings.models import Passenger, Booking


@admin.register(Passenger)
class PassengerAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "email")
    search_fields = ("first_name", "last_name", "email")


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("id", "passenger", "flight", "status")
    list_filter = ("status", "flight")
    search_fields = (
        "passenger__first_name",
        "passenger__last_name",
        "flight__flight_number",
    )
    raw_id_fields = ("passenger", "flight", "booked_by")
