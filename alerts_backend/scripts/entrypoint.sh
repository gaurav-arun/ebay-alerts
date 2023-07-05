#!/bin/bash

set -e

# Apply migrations
python manage.py makemigrations
python manage.py migrate

# Relay control back to the CMD
exec "$@"
