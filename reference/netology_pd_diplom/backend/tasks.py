# tasks.py
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator

@shared_task
def send_email_confirmation(user_id, token):
    user = User.objects.get(id=user_id)
    subject = 'Подтверждение электронной почты'
    message = f'Перейдите по ссылке для подтверждения: {settings.FRONTEND_URL}/confirm-email/?token={token}'
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])

@shared_task
def send_password_reset_email(user_id):
    user = User.objects.get(id=user_id)
    token_generator = PasswordResetTokenGenerator()
    token = token_generator.make_token(user)
    subject = 'Сброс пароля'
    message = f'Для сброса пароля перейдите по ссылке: {settings.FRONTEND_URL}/reset-password/?token={token}'
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])