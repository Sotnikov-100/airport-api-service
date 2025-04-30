#!/bin/bash

set -e

echo "Waiting for PostgreSQL..."
until pg_isready -h "$DB_HOST" -U "$DB_USER"; do
  sleep 1
done

echo "Applying migrations..."
python manage.py migrate

echo "Creating superuser..."
if [ "$DEBUG" = "True" ]; then
  python create_superuser.py
else
  if [ -z "$DJANGO_SUPERUSER_EMAIL" ] || [ -z "$DJANGO_SUPERUSER_PASSWORD" ]; then
    echo "Error: DJANGO_SUPERUSER_EMAIL and DJANGO_SUPERUSER_PASSWORD must be set in production" >&2
    exit 1
  fi
  python create_superuser.py
fi

exec "$@"
