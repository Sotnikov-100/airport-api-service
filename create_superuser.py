import os
import django


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()


def create_admin():
    email = os.getenv("DJANGO_SUPERUSER_EMAIL")
    password = os.getenv("DJANGO_SUPERUSER_PASSWORD")

    if not email or not password:
        if os.getenv("DEBUG", "False") == "True":
            email = "admin@example.com"
            password = "admin"
            print("Using default admin credentials for development")
        else:
            raise ValueError(
                "DJANGO_SUPERUSER_EMAIL and DJANGO_SUPERUSER_PASSWORD must be set in production"
            )

    if not User.objects.filter(email=email).exists():
        print(f"Creating superuser {email}...")
        User.objects.create_superuser(email=email, password=password)
    else:
        print(f"Superuser {email} already exists")


if __name__ == "__main__":
    create_admin()
