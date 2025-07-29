#!/bin/bash
set -e

echo "Waiting for database..."
sleep 2

echo "Running migrations..."
python manage.py makemigrations ledger --noinput
python manage.py migrate --noinput

echo "Initializing test data..."
python init_data.py || echo "Test data initialization skipped"

echo "Starting Django development server..."
python manage.py runserver 0.0.0.0:8000