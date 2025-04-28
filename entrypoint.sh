#!/bin/bash

set -e

echo "Waiting for PostgreSQL to be ready..."
until PGPASSWORD=$DB_PASSWORD psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

echo "Running migrations..."
python manage.py migrate

echo "Creating superuser if not exists..."
python create_superuser.py

echo "Starting Django server..."
exec "$@"
