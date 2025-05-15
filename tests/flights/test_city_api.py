import pytest
from django.urls import reverse
from rest_framework import status
from apps.flights.models import City


@pytest.mark.django_db
class TestCityAPI:
    def test_list_cities(self, authenticated_client, city):
        url = reverse("flights:city-list")
        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert any(
            result["name"] == city.name and result["country"] == city.country.id
            for result in response.data["results"]
        )

    def test_retrieve_airport(self, authenticated_client, airport):
        url = reverse("flights:airport-detail", kwargs={"pk": airport.pk})
        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == airport.name
        assert response.data["code"] == airport.code
        assert response.data["city"] == airport.city.id

    def test_create_city_unauthenticated(self, api_client, country):
        url = reverse("flights:city-list")
        data = {"name": "New City", "country": country.pk}
        response = api_client.post(url, data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_city_admin(self, admin_client, country):
        url = reverse("flights:city-list")
        data = {"name": "New City", "country": country.pk}
        response = admin_client.post(url, data)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["name"] == "New City"
        assert City.objects.filter(name="New City").exists()

    def test_update_city_admin(self, admin_client, city):
        url = reverse("flights:city-detail", kwargs={"pk": city.pk})
        data = {"name": "Updated City", "country": city.country.pk}
        response = admin_client.put(url, data)

        assert response.status_code == status.HTTP_200_OK
        city.refresh_from_db()
        assert city.name == "Updated City"

    def test_delete_city_admin(self, admin_client, city):
        url = reverse("flights:city-detail", kwargs={"pk": city.pk})
        response = admin_client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not City.objects.filter(pk=city.pk).exists()

    def test_create_city_invalid_data(self, admin_client):
        """Test creating city with invalid data fails."""
        url = reverse("flights:city-list")
        data = {"name": "", "country": 9999}
        response = admin_client.post(url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "name" in response.data
        assert "country" in response.data

    def test_update_city_invalid_country(self, admin_client, city):
        """Test updating city with invalid country fails."""
        url = reverse("flights:city-detail", kwargs={"pk": city.pk})
        data = {"country": 9999}
        response = admin_client.patch(url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "country" in response.data
