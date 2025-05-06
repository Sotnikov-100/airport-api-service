import pytest
from django.urls import reverse
from rest_framework import status
from datetime import timedelta
from django.utils import timezone


@pytest.mark.django_db
class TestFlightAPI:
    def test_flight_list(self, authenticated_client, flight):
        url = reverse("flights:flight-list")
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 1
        assert response.data["results"][0]["flight_number"] == flight.flight_number

    def test_flight_retrieve(self, authenticated_client, flight):
        url = reverse("flights:flight-detail", args=[flight.id])
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["flight_number"] == flight.flight_number

    def test_flight_create_as_user_fails(
        self, authenticated_client, airport, airport2, aircraft
    ):
        url = reverse("flights:flight-list")
        data = {
            "flight_number": "TA125",
            "departure_airport": airport.id,
            "arrival_airport": airport2.id,
            "departure_time": (timezone.now() + timedelta(hours=2)).isoformat(),
            "arrival_time": (timezone.now() + timedelta(hours=5)).isoformat(),
            "aircraft": aircraft.id,
            "status": "scheduled",
            "available_seats": 150,
        }
        response = authenticated_client.post(url, data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_flight_filter_by_status(self, authenticated_client, flight):
        url = reverse("flights:flight-list")
        response = authenticated_client.get(url, {"status": "scheduled"})
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 1
        assert response.data["results"][0]["status"] == "scheduled"

    def test_flight_search_action(self, authenticated_client, flight):
        url = reverse("flights:flight-search")
        response = authenticated_client.get(
            url,
            {"from": flight.departure_airport.code, "to": flight.arrival_airport.code},
        )
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]["flight_number"] == flight.flight_number

    def test_flight_search_with_date(self, authenticated_client, flight):
        url = reverse("flights:flight-search")
        date_str = flight.departure_time.date().isoformat()
        response = authenticated_client.get(
            url,
            {
                "from": flight.departure_airport.code,
                "to": flight.arrival_airport.code,
                "date": date_str,
            },
        )
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

    def test_flight_upcoming_action(self, authenticated_client, flight):
        url = reverse("flights:flight-upcoming")
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 1

    def test_flight_statistics_action(self, admin_client, flight):
        url = reverse("flights:flight-statistics")
        response = admin_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert any(stat["status"] == "scheduled" for stat in response.data)

    def test_flight_update_status_action(self, admin_client, flight):
        url = reverse("flights:flight-update-status", args=[flight.id])
        response = admin_client.post(url, {"status": "delayed"})
        assert response.status_code == status.HTTP_200_OK
        assert response.data["status"] == "delayed"

    def test_flight_available_seats_action(self, authenticated_client, flight):
        url = reverse("flights:flight-available-seats", args=[flight.id])
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["available_seats"] == flight.available_seats
