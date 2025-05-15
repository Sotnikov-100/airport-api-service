import pytest
from django.urls import reverse
from rest_framework import status
from apps.bookings.models import Booking
from apps.users.models import User


@pytest.mark.django_db
class TestBookingAPI:
    def test_create_booking(self, authenticated_client, flight, passenger, user):
        url = reverse("bookings:booking-list")
        data = {
            "flight_id": flight.id,
            "passenger_id": passenger.id,
            "seat_number": "15B",
        }
        response = authenticated_client.post(url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert Booking.objects.count() == 1
        booking = Booking.objects.get()
        assert booking.seat_number == "15B"
        assert booking.booked_by == user

    def test_list_bookings(self, authenticated_client, booking, user):
        url = reverse("bookings:booking-list")
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 1
        assert response.data["results"][0]["seat_number"] == booking.seat_number

    def test_list_bookings_admin(self, admin_client, booking):
        url = reverse("bookings:booking-list")
        response = admin_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 1

    def test_retrieve_booking(self, authenticated_client, booking):
        url = reverse("bookings:booking-detail", kwargs={"pk": booking.pk})
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["seat_number"] == booking.seat_number
        assert response.data["flight"]["flight_number"] == booking.flight.flight_number

    def test_update_booking(self, authenticated_client, booking):
        url = reverse("bookings:booking-detail", kwargs={"pk": booking.pk})
        data = {"seat_number": "20C"}
        response = authenticated_client.patch(url, data, format="json")
        assert response.status_code == status.HTTP_200_OK
        booking.refresh_from_db()
        assert booking.seat_number == "20C"

    def test_cannot_update_other_users_booking(
        self, authenticated_client, booking, user
    ):
        another_user = User.objects.create_user(
            email="another@example.com",
            password="testpass",
            first_name="Another",
            last_name="User",
        )
        another_booking = Booking.objects.create(
            flight=booking.flight,
            passenger=booking.passenger,
            seat_number="10A",
            status="confirmed",
            booked_by=another_user,
        )

        url = reverse("bookings:booking-detail", kwargs={"pk": another_booking.pk})
        data = {"seat_number": "20D"}
        response = authenticated_client.patch(url, data, format="json")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_admin_can_update_any_booking(self, admin_client, booking):
        url = reverse("bookings:booking-detail", kwargs={"pk": booking.pk})
        data = {"seat_number": "1A", "status": "completed"}
        response = admin_client.patch(url, data, format="json")
        assert response.status_code == status.HTTP_200_OK
        booking.refresh_from_db()
        assert booking.seat_number == "1A"
        assert booking.status == "completed"

    def test_delete_booking(self, authenticated_client, booking):
        url = reverse("bookings:booking-detail", kwargs={"pk": booking.pk})
        response = authenticated_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Booking.objects.count() == 0

    def test_create_booking_invalid_flight(self, authenticated_client, passenger):
        """Test creating booking with invalid flight fails."""
        url = reverse("bookings:booking-list")
        data = {
            "flight_id": 9999,
            "passenger_id": passenger.id,
            "seat_number": "15B",
        }
        response = authenticated_client.post(url, data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_delete_nonexistent_booking(self, authenticated_client):
        """Test deleting non-existent booking fails."""
        url = reverse("bookings:booking-detail", kwargs={"pk": 9999})
        response = authenticated_client.delete(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND
