#!/bin/bash

# Run collectstatic to gather static files
python manage.py collectstatic --noinput
ls -la ./staticfiles_build

# Run the default CMD (start Gunicorn)
exec "$@"
