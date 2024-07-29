from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from logging import getLogger
from random import randint

logger = getLogger('base-logger')


@shared_task(ignore_result=True)
def get_verify_code(recipient_email: str):
    verify_code = ''.join([str(randint(0, 9)) for _ in range(6)])

    send_mail(subject="Код подтверждения", from_email=settings.DEFAULT_FROM_EMAIL,
        message=f"Код подтверждения: {verify_code}", recipient_list=[recipient_email])
