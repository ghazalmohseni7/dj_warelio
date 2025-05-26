#!/bin/bash
echo "Ensuring directories exist..."
mkdir -p /Warelio/static

echo "Applying database migrations..."
python manage.py makemigrations
python manage.py migrate

# Create superuser if it doesn’t exist
echo "Creating superuser..."
python manage.py shell <<EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin')
    print("Superuser created.")
else:
    print("Superuser already exists.")
EOF

echo "Collecting static files..."
python manage.py collectstatic --noinput

# Run Django, pubsub scripts in the background
echo "Starting services..."
/Warelio/bashes/start_django.sh &
/Warelio/bashes/start_pubsub_subscriber.sh &

# Keep container running
wait