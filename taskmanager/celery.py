from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from datetime import timedelta

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'taskmanager.settings')

app = Celery('taskmanager')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


# Celery Beat Settings
app.conf.beat_schedule = {
    "send-test-email": {
        "task": "taskmanager.tasks.send_test_email",
        "schedule": timedelta(seconds=10),
        "args": ()
    },
}

