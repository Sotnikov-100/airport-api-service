import pytest
from django.urls import reverse
from rest_framework import status
from apps.users.models import User
from tests.conftest import api_client


@pytest.mark.django_db
class TestUserAPI:
    def test_user_registration(self, api_client):
        """Test user registration."""
        url = reverse("users:register")
        data = {
            "email": "newuser@example.com",
            "password": "securepassword123",
            "first_name": "New",
            "last_name": "User",
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        user = User.objects.get(email="newuser@example.com")
        assert user.first_name == "New"
        assert user.last_name == "User"
        assert user.check_password("securepassword123")

    def test_duplicate_email_registration(self, api_client, user):
        """Test registration with duplicate email fails."""
        url = reverse("users:register")
        data = {
            "email": user.email,
            "password": "anotherpassword",
            "first_name": "Another",
            "last_name": "User",
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "email" in response.data

    def test_token_obtain(self, api_client, user):
        """Test obtaining token pair."""
        url = reverse("users:token_obtain_pair")
        data = {"email": "test@example.com", "password": "testpassword"}
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data
        assert "refresh" in response.data

    def test_token_obtain_invalid_credentials(self, api_client):
        """Test obtaining token with invalid credentials fails."""
        url = reverse("users:token_obtain_pair")
        data = {"email": "nonexistent@example.com", "password": "wrongpassword"}
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_token_refresh(self, api_client, user_token):
        """Test refreshing access token."""
        url = reverse("users:token_refresh")
        data = {"refresh": user_token["refresh"]}
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data

    def test_token_refresh_invalid(self, api_client):
        """Test refreshing with invalid token fails."""
        url = reverse("users:token_refresh")
        data = {"refresh": "invalid-token"}
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_access_protected_endpoint(self, authenticated_client):
        """Test accessing a protected endpoint with valid token."""
        url = reverse("bookings:booking-list")
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_registration_with_minimal_data(self, api_client):
        """Test user registration with only required fields."""
        url = reverse("users:register")
        data = {"email": "minimal@example.com", "password": "minimalpassword"}
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        user = User.objects.get(email="minimal@example.com")
        assert user.first_name == ""
        assert user.last_name == ""

    def test_registration_with_invalid_email(self, api_client):
        """Test registration with invalid email format fails."""
        url = reverse("users:register")
        data = {"email": "not-an-email", "password": "validpassword"}
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "email" in response.data


    def test_token_obtain_missing_credentials(self, api_client):
        """Test obtaining token with missing credentials fails."""
        url = reverse("users:token_obtain_pair")
        data = {}
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "email" in response.data
        assert "password" in response.data
