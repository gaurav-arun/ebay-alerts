#!/bin/bash

set -e

echo "Applying database migrations..."
# TODO: Add --noinput flag to migration commands
python manage.py makemigrations --noinput
python manage.py migrate --noinput

echo "Generating swagger schema..."
python manage.py spectacular --color --file schema.yml

echo "All Done!!"

# Relay control back to the CMD
exec "$@"