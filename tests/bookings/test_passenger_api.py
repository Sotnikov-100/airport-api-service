import pytest
from django.urls import reverse
from rest_framework import status
from apps.bookings.models import Passenger


@pytest.mark.django_db
class TestPassengerAPI:
    def test_create_passenger(self, authenticated_client):
        url = reverse("bookings:passenger-list")
        data = {
            "first_name": "Jane",
            "last_name": "Smith",
            "email": "jane.smith@example.com",
            "phone": "+1234567890",
        }
        response = authenticated_client.post(url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert Passenger.objects.count() == 1
        assert Passenger.objects.get().first_name == "Jane"

    def test_list_passengers(self, authenticated_client, passenger):
        url = reverse("bookings:passenger-list")
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 1
        assert response.data["results"][0]["first_name"] == passenger.first_name

    def test_retrieve_passenger(self, authenticated_client, passenger):
        url = reverse("bookings:passenger-detail", kwargs={"pk": passenger.pk})
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["first_name"] == passenger.first_name
        assert response.data["email"] == passenger.email

    def test_update_passenger(self, authenticated_client, passenger):
        url = reverse("bookings:passenger-detail", kwargs={"pk": passenger.pk})
        data = {
            "first_name": "Updated",
            "last_name": passenger.last_name,
            "email": passenger.email,
        }
        response = authenticated_client.patch(url, data, format="json")
        assert response.status_code == status.HTTP_200_OK
        passenger.refresh_from_db()
        assert passenger.first_name == "Updated"

    def test_delete_passenger(self, authenticated_client, passenger):
        url = reverse("bookings:passenger-detail", kwargs={"pk": passenger.pk})
        response = authenticated_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Passenger.objects.count() == 0

    def test_create_passenger_invalid_data(self, authenticated_client):
        """Test creating passenger with invalid data fails."""
        url = reverse("bookings:passenger-list")
        data = {
            "first_name": "",
            "email": "not-an-email",
        }
        response = authenticated_client.post(url, data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "first_name" in response.data
        assert "email" in response.data

    def test_update_passenger_invalid_data(self, authenticated_client, passenger):
        """Test updating passenger with invalid data fails."""
        url = reverse("bookings:passenger-detail", kwargs={"pk": passenger.pk})
        data = {"email": ""}
        response = authenticated_client.patch(url, data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "email" in response.data
