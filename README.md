###################### Celery Setup ########################

1. Install redis server and celery and start celery worker process and see logs.
   
    # Installing redis server(you can also use rabbitMQ,I am using redis server): 
     
        1. sudo apt update
        2. sudo apt install redis-server
        3. sudo systemctl enable redis-server
        4. sudo systemctl restart redis-server
        5. sudo systemctl status redis-server # Ensure its status is running.
    
    # Install celery and redis in django project environemnt.

        1. pip install redis
        2. pip install celery

    # Start Celery worker process and see logs:

        1. celery -A queuemanager worker --loglevel=info    #'queuemanager' is your project name

2. Configure the following settings in your settings.py file.

        # settings.py

        CELERY_BROKER_URL = 'redis://localhost:6379/0'  
        CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
        CELERY_ACCEPT_CONTENT = ['json']
        CELERY_TASK_SERIALIZER = 'json'
        CELERY_RESULT_SERIALIZER = 'json'
        CELERY_TIMEZONE = 'Asia/Kolkata'
        CELERY_ACKS_LATE = True 


3. Create a celery.py file with the following code in the project directory where settings.py is located.


        from __future__ import absolute_import, unicode_literals
        import os
        from celery import Celery

        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'queuemanager.settings')
        app = Celery('queuemanager')
        app.config_from_object('django.conf:settings', namespace='CELERY')
        app.autodiscover_tasks()

    
4. Add the following code to the __init__.py file of the project.

        from .celery import app as celery_app
        __all__ = ('celery_app',)

5. Create tasks.py file in the project folder (you can create it in any app) and define a task using @shared_taskdecorator.

        from celery import shared_task
        from django.core.mail import send_mail

        @shared_task
        def send_test_email():
            subject = 'Test Email'
            message = 'This is a test email sent from Django.'
            from_email = 'dsfadf@gmail.com'
            recipient_list = ['dfjdlfk@gmail.com']
            send_mail(subject, message, from_email, recipient_list)


6. Now you can call this task in the API where you want to use it.

        from rest_framework.views import APIView
        from rest_framework.response import Response
        from queuemanager.tasks import send_test_email

        class ExecuteTask(APIView):
            @staticmethod
            def get(request):
                send_test_email.apply_async()
                return Response({"success": "True", "message": "executed successfully", "data": []})

7. That's it! Hit the endpoint of the 'ExecuteTask' API, and you will see the logs received using the command \ 
   "celery -A queuemanager worker --loglevel=info"



########################## Celery Beat Setup ########################   

Note: The Celery setup should be completed before setting up Celery Beat.

1. Install django-celery-beat in your Django project environment, include it in INSTALLED_APPS, and migrate.
   
       1. pip install django-celery-beat

       2. INSTALLED_APPS = [
            ...
            'django_celery_beat',
            ...
          ]
       3. python manage.py migrate django_celery_beat

2. Update your Celery configuration in settins.py file

        #Celery config
        CELERY_BROKER_URL = 'redis://localhost:6379/0'  
        CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
        CELERY_ACCEPT_CONTENT = ['json']
        CELERY_TASK_SERIALIZER = 'json'
        CELERY_RESULT_SERIALIZER = 'json'
        CELERY_TIMEZONE = 'Asia/Kolkata'
        CELERY_ACKS_LATE = True 

        #CeleryBeat config
        CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'    # add this one..

   
3. Create periodic tasks in celery.py file by following block of code:

            # Celery Beat Settings
            app.conf.beat_schedule = {
                "send-test-email": {
                    "task": "queuemanager.tasks.send_test_email",
                    "schedule": timedelta(seconds=10),
                    "args": ()
                },
            }

        
        #updated celery.py 

        from __future__ import absolute_import, unicode_literals
        import os
        from celery import Celery
        from datetime import timedelta

        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'queuemanager.settings')
        app = Celery('queuemanager')
        app.config_from_object('django.conf:settings', namespace='CELERY')
        app.autodiscover_tasks()

        app.conf.beat_schedule = {
            "send-test-email": {
                "task": "queuemanager.tasks.send_test_email",
                "schedule": timedelta(seconds=10),
                "args": ()
            },
        }

4. Make sure both of the following commands are running. That's it.

        # Start Celery worker
        celery -A queuemanager worker -l info

        # Start Celery beat
        celery -A queuemanager beat -l info
