#!/bin/sh

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate

echo "Apply cities_light migrations"
python manage.py cities_light

# Start server
echo "Starting server"
python manage.py runserver 0.0.0.0:8000
