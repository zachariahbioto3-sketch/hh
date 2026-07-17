import os
import django
import psycopg2
from django.core.management import call_command

# Set Render's DATABASE_URL temporarily
os.environ['DATABASE_URL'] = 'YOUR_POSTGRES_URL_HERE'  # Replace with actual URL from Render
os.environ['DJANGO_SETTINGS_MODULE'] = 'association_site.settings'

django.setup()

# Load the fixture into Render's Postgres
call_command('loaddata', 'db_backup.json')
print("Data loaded successfully!")
