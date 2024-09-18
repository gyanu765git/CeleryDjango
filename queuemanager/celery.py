# queuemanager/celery.py

from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'queuemanager.settings')

app = Celery('queuemanager')

# Use a string here; the worker doesn't need to serialize the configuration
app.config_from_object('django.conf:settings', namespace='CELERY')

# Discover tasks in all installed Django apps
app.autodiscover_tasks()
