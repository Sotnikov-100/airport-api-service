import pytest
from django.urls import reverse
from rest_framework import status
from apps.flights.models import Airport


@pytest.mark.django_db
class TestAirportAPI:
    def test_airport_list(self, authenticated_client, airport):
        url = reverse("flights:airport-list")
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 1
        assert response.data["results"][0]["code"] == airport.code

    def test_retrieve_airport(self, authenticated_client, airport):
        url = reverse("flights:airport-detail", kwargs={"pk": airport.pk})
        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == airport.name
        assert response.data["code"] == airport.code
        assert response.data["city"] == airport.city.id

    def test_create_airport_unauthenticated(self, api_client, city):
        url = reverse("flights:airport-list")
        data = {"name": "New Airport", "code": "NEW", "city": city.pk}
        response = api_client.post(url, data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_airport_admin(self, admin_client, city):
        url = reverse("flights:airport-list")
        data = {"name": "New Airport", "code": "NEW", "city": city.pk}
        response = admin_client.post(url, data)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["name"] == "New Airport"
        assert response.data["code"] == "NEW"
        assert Airport.objects.filter(code="NEW").exists()

    def test_update_airport_admin(self, admin_client, airport):
        url = reverse("flights:airport-detail", kwargs={"pk": airport.pk})
        data = {
            "name": "Updated Airport",
            "code": airport.code,
            "city": airport.city.pk,
        }
        response = admin_client.put(url, data)

        assert response.status_code == status.HTTP_200_OK
        airport.refresh_from_db()
        assert airport.name == "Updated Airport"

    def test_delete_airport_admin(self, admin_client, airport):
        url = reverse("flights:airport-detail", kwargs={"pk": airport.pk})
        response = admin_client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Airport.objects.filter(pk=airport.pk).exists()

    def test_create_airport_invalid_data(self, admin_client):
        """Test creating airport with invalid data fails."""
        url = reverse("flights:airport-list")
        data = {"name": "", "code": "INVALIDCODE", "city": 9999}
        response = admin_client.post(url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "name" in response.data
        assert "code" in response.data
        assert "city" in response.data

    def test_update_airport_invalid_data(self, admin_client, airport):
        """Test updating airport with invalid data fails."""
        url = reverse("flights:airport-detail", kwargs={"pk": airport.pk})
        data = {"code": "TOOLONGCODE"}
        response = admin_client.patch(url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "code" in response.data
