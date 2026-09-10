#!/usr/bin/env bash
set -o errexit
pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate
python manage.py shell -c "
from django.contrib.auth import get_user_model
import os
User = get_user_model()
print('Total users:', User.objects.count())
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@kafuosa.com', os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'changeme'))
    print('Superuser created successfully')
else:
    print('Admin already exists')
"
