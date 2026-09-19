#!/usr/bin/env bash
set -o errexit
pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate
python manage.py shell -c "
from django.contrib.auth import get_user_model
import os
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@kafuosa.com', 'AdminKafuosa2024')
    print('Superuser created')
else:
    u = User.objects.get(username='admin')
    u.set_password('AdminKafuosa2024')
    u.is_staff = True
    u.is_superuser = True
    u.save()
    print('Admin password reset done')
"
