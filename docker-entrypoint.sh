#!/bin/bash
set -e

echo "Running Migrations"
# Run collectstatic
python manage.py collectstatic --noinput
# Run migrations
python manage.py migrate --noinput

echo "Starting application .. .. "
daphne -b 0.0.0.0 -p 8000 hashchat.asgi:application