###################### Celery Setup ########################

1. install redis server and celery.
   
    # installing redis server( you can also use rabbitMQ), I am using redis server
     
        1. sudo apt update
        2. sudo apt install redis-server
        3. sudo systemctl enable redis-server
        4. sudo systemctl restart redis-server
        5. sudo systemctl status redis-server # make sure it status is running....
    
    # install celery and redis in django project environemnt.

        1. pip install redis
        2. pip install celery

2. Do following settings configuration in your project settings.py file.

        # settings.py

        CELERY_BROKER_URL = 'redis://localhost:6379/0'  
        CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
        CELERY_ACCEPT_CONTENT = ['json']
        CELERY_TASK_SERIALIZER = 'json'
        CELERY_RESULT_SERIALIZER = 'json'
        CELERY_TIMEZONE = 'Asia/Kolkata'
        CELERY_ACKS_LATE = True 


3. Create celery.py file with following block of code in project directory where settings.py file located.


        from __future__ import absolute_import, unicode_literals
        import os
        from celery import Celery

        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'queuemanager.settings')
        app = Celery('queuemanager')
        app.config_from_object('django.conf:settings', namespace='CELERY')
        app.autodiscover_tasks()

    
4. Paste below block of code in __init__.py file of project.

        from .celery import app as celery_app
        __all__ = ('celery_app',)

5. Create tasks.py file in project folder( you can create it in any app) and create task using @shared_task decorator.

        from celery import shared_task
        from django.core.mail import send_mail

        @shared_task
        def send_test_email():
            subject = 'Test Email'
            message = 'This is a test email sent from Django.'
            from_email = 'dsfadf@gmail.com'
            recipient_list = ['dfjdlfk@gmail.com']
            send_mail(subject, message, from_email, recipient_list)


6. Now you can call this task in api you want to use.

        from rest_framework.views import APIView
        from rest_framework.response import Response
        from queuemanager.tasks import send_test_email

        class ExecuteTask(APIView):
            @staticmethod
            def get(request):
                send_test_email.apply_async()
                return Response({"success": "True", "message": "executed successfully", "data": []})

