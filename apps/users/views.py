from rest_framework import generics, permissions
from drf_spectacular.utils import extend_schema

from apps.users.models import User
from apps.users.serializers import UserRegistrationSerializer


@extend_schema(
    summary="Register a new user",
    description="Create a new user account with username, email, and password",
    tags=["Authentication"],
    responses={201: UserRegistrationSerializer},
)
class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(serializer.validated_data["password"])
        user.save()
