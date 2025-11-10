#!/bin/bash

set -o errexit

# Run migrations
echo "Making migrations...."
python manage.py makemigrations

echo "Applying migrations..."
python manage.py migrate

echo "Prepopulating learning levels..."
python manage.py populate_learning_levels

echo "Prepopulating learning areas....."
python manage.py populate_cbc_learning_areas

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Start the application
echo "Starting application..."
exec gunicorn acerschoolappapi.wsgi:application --bind 0.0.0.0:8000 --timeout 180
