import os
import django


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "admin@example.com")
password = os.environ.get("DJANGO_SUPERUSER_PASSWORD", "admin")

if not User.objects.filter(email=email).exists():
    print(f"Creating superuser {email}...")
    User.objects.create_superuser(email=email, password=password)
else:
    print(f"Superuser {email} already exists.")
