#!/bin/bash

set -e

# Apply migrations
python manage.py makemigrations
python manage.py migrate

echo "Generating swagger schema..."
python manage.py spectacular --color --file schema.yml

echo "Running celery worker & beat..."
python -m celery -A alerts_backend worker -E -l INFO
python -m celery -A alerts_backend beat -E -l INFO

echo "All Done!!"

# Relay control back to the CMD
exec "$@"
