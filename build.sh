#!/bin/bash
# Collect static files
python manage.py collectstatic --noinput

# Apply migrations
python manage.py migrate 