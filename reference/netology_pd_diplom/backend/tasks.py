# tasks.py
from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.dispatch import receiver
from backend.signals import reset_password_token_created


@shared_task
def send_password_reset_email(user_email, token_key):
    """
    Задача Celery для отправки электронного письма с токеном сброса пароля.

    :param user_email: Email пользователя
    :param token_key: Токен для сброса пароля
    """
    msg = EmailMultiAlternatives(
        # Заголовок письма
        f"Password Reset Token for {user_email}",
        # Сообщение
        token_key,
        # Email отправителя
        settings.EMAIL_HOST_USER,
        # Email получателя
        [user_email]
    )
    msg.send()


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, **kwargs):
    """
    Обработчик сигнала, который запускает отправку письма с токеном для сброса пароля.

    :param sender: Класс View, который отправил сигнал
    :param instance: Экземпляр View, который отправил сигнал
    :param reset_password_token: Объект модели токена
    :param kwargs:
    :return:
    """
    # Вызываем асинхронную задачу для отправки электронной почты
    send_password_reset_email.delay(reset_password_token.user.email, reset_password_token.key)