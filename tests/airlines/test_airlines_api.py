import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestAirlineAPI:
    def test_airline_list(self, authenticated_client, airline):
        url = reverse("airlines:airlines-list")
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 1
        assert response.data["results"][0]["name"] == airline.name

    def test_airline_retrieve(self, authenticated_client, airline):
        url = reverse("airlines:airlines-detail", args=[airline.id])
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == airline.name
        assert response.data["code"] == airline.code

    def test_airline_create_as_admin(self, admin_client):
        url = reverse("airlines:airlines-list")
        data = {"name": "New Airline", "code": "NA"}
        response = admin_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["name"] == "New Airline"

    def test_airline_create_as_user_fails(self, authenticated_client):
        url = reverse("airlines:airlines-list")
        data = {"name": "New Airline", "code": "NA"}
        response = authenticated_client.post(url, data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_airline_update_as_admin(self, admin_client, airline):
        url = reverse("airlines:airlines-detail", args=[airline.id])
        data = {"name": "Updated Airline", "code": airline.code}
        response = admin_client.patch(url, data)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == "Updated Airline"

    def test_airline_delete_as_admin(self, admin_client, airline):
        url = reverse("airlines:airlines-detail", args=[airline.id])
        response = admin_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_airline_create_invalid_data(self, admin_client):
        """Test creating airline with invalid data fails."""
        url = reverse("airlines:airlines-list")
        data = {"name": "", "code": "TOOLONG"}
        response = admin_client.post(url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "name" in response.data
        assert "code" in response.data

    def test_airline_update_invalid_data(self, admin_client, airline):
        """Test updating airline with invalid data fails."""
        url = reverse("airlines:airlines-detail", args=[airline.id])
        data = {"code": ""}
        response = admin_client.patch(url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "code" in response.data
