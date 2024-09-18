from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_test_email():
    subject = 'Test Email'
    message = 'This is a test email sent from Django.'
    from_email = 'gifafjfij@gmail.com'
    recipient_list = ['dfakldjfkl@gmail.com']
    send_mail(subject, message, from_email, recipient_list)
