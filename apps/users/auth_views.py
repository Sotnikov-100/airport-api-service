from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.utils import extend_schema, OpenApiResponse, inline_serializer
from rest_framework import serializers, status


@extend_schema(
    summary="Get JWT token",
    description="Obtain JWT token pair with username and password",
    tags=["Authentication"],
    responses={
        status.HTTP_200_OK: inline_serializer(
            name="TokenObtainPairResponse",
            fields={
                "access": serializers.CharField(),
                "refresh": serializers.CharField(),
            },
        ),
        status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
            description="Authentication failed",
        ),
    },
)
class CustomTokenObtainPairView(TokenObtainPairView):
    pass


@extend_schema(
    summary="Refresh JWT token",
    description="Refresh JWT access token using refresh token",
    tags=["Authentication"],
    responses={
        status.HTTP_200_OK: inline_serializer(
            name="TokenRefreshResponse",
            fields={
                "access": serializers.CharField(),
            },
        ),
        status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
            description="Invalid or expired refresh token",
        ),
    },
)
class CustomTokenRefreshView(TokenRefreshView):
    pass
