#!/bin/sh
set -e
python manage.py migrate --noinput
python manage.py seed_loadtest
python manage.py collectstatic --noinput
exec gunicorn demo_project.wsgi:application --bind 0.0.0.0:8000
