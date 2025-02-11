from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from backend.models import ConfirmEmailToken, User

@shared_task
def send_password_reset_email(user_email, token):
    msg = EmailMultiAlternatives(
        f"Password Reset Token for {user_email}",
        token,
        settings.EMAIL_HOST_USER,
        [user_email]
    )
    msg.send()

@shared_task
def send_email_confirmation(user_id):
    user = User.objects.get(id=user_id)
    token, _ = ConfirmEmailToken.objects.get_or_create(user_id=user_id)
    msg = EmailMultiAlternatives(
        f"Password Reset Token for {user.email}",
        token.key,
        settings.EMAIL_HOST_USER,
        [user.email]
    )
    msg.send()

@shared_task
def send_order_status_update(user_id):
    user = User.objects.get(id=user_id)
    msg = EmailMultiAlternatives(
        f"Обновление статуса заказа",
        'Заказ сформирован',
        settings.EMAIL_HOST_USER,
        [user.email]
    )
    msg.send()

@shared_task
def send_new_order_notification(user_id):
    """
    Отправляет уведомление о новом заказе.
    """
    user = User.objects.get(id=user_id)
    msg = EmailMultiAlternatives(
        subject="Новый заказ",
        body="Ваш заказ успешно оформлен.",
        from_email=settings.EMAIL_HOST_USER,
        to=[user.email]
    )
    msg.send()