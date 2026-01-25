#!/usr/bin/env bash
set -o errexit
pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate

# Create superuser if it doesn't exist (for Render deployment)
python manage.py shell -c "
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@numeneon.com', 'admin123')
    print('Superuser created: admin / admin123')
else:
    print('Superuser already exists')
"

# Create test user pabloPistola if it doesn't exist
python manage.py shell -c "
from django.contrib.auth.models import User
if not User.objects.filter(username='pabloPistola').exists():
    User.objects.create_user('pabloPistola', 'pablo@test.com', 'test123')
    print('Test user created: pabloPistola / test123')
else:
    print('Test user pabloPistola already exists')
"
