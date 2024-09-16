#!/bin/bash

echo "Appling database migrations..."
python manage.py migrate

exec "$@"