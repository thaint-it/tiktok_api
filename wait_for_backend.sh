#!/bin/sh
# wait_for_backend.sh

# Wait for the backend service to be ready
while ! nc -z backend 8000; do   
  sleep 1 # wait for 1 second before checking again
done
echo "Backend is up!"

# Start the ASGI server
daphne tiktok_api.asgi:application -b 0.0.0.0 -p 9000
