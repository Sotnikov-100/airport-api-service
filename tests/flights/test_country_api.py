import pytest
from django.urls import reverse
from rest_framework import status
from apps.flights.models import Country


@pytest.mark.django_db
class TestCountryAPI:
    def test_country_list(self, authenticated_client, country):
        url = reverse("flights:country-list")
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 1
        assert response.data["results"][0]["code"] == country.code

    def test_retrieve_country(self, authenticated_client, country):
        url = reverse("flights:country-detail", kwargs={"pk": country.pk})
        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == country.name
        assert response.data["code"] == country.code

    def test_create_country_unauthenticated(self, api_client):
        url = reverse("flights:country-list")
        data = {"name": "New Country", "code": "NC"}
        response = api_client.post(url, data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_country_admin(self, admin_client):
        url = reverse("flights:country-list")
        data = {"name": "New Country", "code": "NC"}
        response = admin_client.post(url, data)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["name"] == "New Country"
        assert response.data["code"] == "NC"
        assert Country.objects.filter(code="NC").exists()

    def test_update_country_admin(self, admin_client, country):
        url = reverse("flights:country-detail", kwargs={"pk": country.pk})
        data = {"name": "Updated Country", "code": country.code}
        response = admin_client.put(url, data)

        assert response.status_code == status.HTTP_200_OK
        country.refresh_from_db()
        assert country.name == "Updated Country"

    def test_delete_country_admin(self, admin_client, country):
        url = reverse("flights:country-detail", kwargs={"pk": country.pk})
        response = admin_client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Country.objects.filter(pk=country.pk).exists()
