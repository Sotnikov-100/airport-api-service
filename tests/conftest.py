import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from apps.users.models import User
from apps.airlines.models import Airline, Aircraft
from apps.flights.models import Country, City, Airport, Flight
from apps.bookings.models import Passenger, Booking
from datetime import timedelta
from django.utils import timezone


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user():
    return User.objects.create_user(
        email="test@example.com",
        password="testpassword",
        first_name="Test",
        last_name="User",
    )


@pytest.fixture
def admin_user():
    return User.objects.create_superuser(
        email="admin@example.com",
        password="adminpassword",
        first_name="Admin",
        last_name="User",
    )


@pytest.fixture
def user_token(user):
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


@pytest.fixture
def admin_token(admin_user):
    refresh = RefreshToken.for_user(admin_user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


@pytest.fixture
def authenticated_client(user_token):
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {user_token['access']}")
    return client


@pytest.fixture
def admin_client(admin_token):
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {admin_token['access']}")
    return client


@pytest.fixture
def api_client_with_credentials(user, api_client):
    token = AccessToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    return api_client


# Airlines fixtures
@pytest.fixture
def airline():
    return Airline.objects.create(name="Test Airline", code="TA")


@pytest.fixture
def aircraft(airline):
    return Aircraft.objects.create(model="Boeing 737", airline=airline)


# Flights fixtures
@pytest.fixture
def country():
    return Country.objects.create(name="Test Country", code="TC")


@pytest.fixture
def city(country):
    return City.objects.create(name="Test City", country=country)


@pytest.fixture
def airport(city):
    return Airport.objects.create(name="Test Airport", code="TST", city=city)


@pytest.fixture
def airport2(city):
    return Airport.objects.create(name="Test Airport 2", code="TS2", city=city)


@pytest.fixture
def flight(airport, airport2, aircraft):
    departure_time = timezone.now() + timedelta(hours=2)
    arrival_time = departure_time + timedelta(hours=3)
    return Flight.objects.create(
        flight_number="TA123",
        departure_airport=airport,
        arrival_airport=airport2,
        departure_time=departure_time,
        arrival_time=arrival_time,
        aircraft=aircraft,
        status="scheduled",
        available_seats=100,
    )


# Bookings fixtures
@pytest.fixture
def passenger():
    return Passenger.objects.create(
        first_name="John",
        last_name="Doe",
        email="john.doe@example.com",
        phone="+1234567890",
    )


@pytest.fixture
def booking(flight, passenger, user):
    return Booking.objects.create(
        flight=flight,
        passenger=passenger,
        seat_number="12A",
        status="confirmed",
        booked_by=user,
    )
