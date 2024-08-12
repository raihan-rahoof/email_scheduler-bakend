from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task(bind=True)
def send_registration_email(to_email,subject,message):
    from_email = settings.EMAIL_HOST_USER
    send_mail(subject,message,from_email,[to_email])
    return 'Done'