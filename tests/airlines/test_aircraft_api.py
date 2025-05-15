import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestAircraftAPI:
    def test_aircraft_list(self, authenticated_client, aircraft):
        url = reverse("airlines:aircrafts-list")
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 1
        assert response.data["results"][0]["model"] == aircraft.model

    def test_aircraft_retrieve(self, authenticated_client, aircraft):
        url = reverse("airlines:aircrafts-detail", args=[aircraft.id])
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["model"] == aircraft.model
        assert response.data["airline"] == aircraft.airline.id

    def test_aircraft_create_as_admin(self, admin_client, airline):
        url = reverse("airlines:aircrafts-list")
        data = {"model": "Airbus A320", "airline": airline.id}
        response = admin_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["model"] == "Airbus A320"

    def test_aircraft_filter_by_airline(self, authenticated_client, aircraft, airline):
        url = reverse("airlines:aircrafts-list")
        response = authenticated_client.get(url, {"airline": airline.id})
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 1
        assert response.data["results"][0]["model"] == aircraft.model

    def test_aircraft_search(self, authenticated_client, aircraft):
        url = reverse("airlines:aircrafts-list")
        response = authenticated_client.get(url, {"search": aircraft.model})
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 1
        assert aircraft.model in response.data["results"][0]["model"]

    def test_aircraft_create_invalid_data(self, admin_client):
        """Test creating aircraft with invalid data fails."""
        url = reverse("airlines:aircrafts-list")
        data = {"model": "", "airline": 9999}
        response = admin_client.post(url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "model" in response.data
        assert "airline" in response.data

    def test_aircraft_filter_invalid_airline(self, authenticated_client):
        """Test filtering aircraft by invalid airline fails."""
        url = reverse("airlines:aircrafts-list")
        response = authenticated_client.get(url, {"airline": "invalid"})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "airline" in response.data
