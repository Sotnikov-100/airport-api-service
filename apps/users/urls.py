from django.urls import path
from rest_framework_simplejwt.views import TokenBlacklistView

from apps.users.views import UserRegistrationView
from apps.users.auth_views import CustomTokenObtainPairView, CustomTokenRefreshView


app_name = "users"

urlpatterns = [
    path("register/", UserRegistrationView.as_view(), name="register"),
    path("token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", CustomTokenRefreshView.as_view(), name="token_refresh"),
    path("token/blacklist/", TokenBlacklistView.as_view(), name="token_blacklist"),
]
