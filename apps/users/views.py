from rest_framework import generics, permissions

from apps.users.models import User
from apps.users.serializers import UserRegistrationSerializer
from apps.users.schemas import user_registration_schema


class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    user_registration_schema = user_registration_schema

    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(serializer.validated_data["password"])
        user.save()
