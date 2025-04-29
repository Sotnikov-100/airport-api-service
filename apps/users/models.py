from django.contrib.auth.models import AbstractUser
from django.db import models
from apps.users.managers import UserManager


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        app_label = "users"

    def __str__(self):
        return self.email
