#!/bin/bash

set -e

echo "Applying database migrations..."
# TODO: Add --noinput flag to migration commands
python manage.py makemigrations
python manage.py migrate

echo "Generating swagger schema..."
python manage.py spectacular --color --file schema.yml

echo "All Done!!"

# Relay control back to the CMD
exec "$@"