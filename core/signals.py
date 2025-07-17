from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from datetime import timedelta
from django.utils import timezone
from .models import Review, Order
from .mystral import is_bad_review
from .telegram_bot import send_telegram_message
from barbershop.settings import TELEGRAM_BOT_API_KEY, TELEGRAM_USER_ID

import pytz

# Получаем нужный часовой пояс
time_zone = pytz.timezone('Europe/Moscow')  # Замените на нужный часовой пояс
import asyncio



@receiver(post_save, sender=Review)
def check_review(sender, instance, created, **kwargs):
    # Created - это флаг, который показывает, что запись была создана
    if created:
        # Меняем статус на ai_checked_in_progress
        instance.ai_checked_status = "ai_checked_in_progress"
        instance.save()

        # Отправляем на проверку
        review_text = instance.text
        if is_bad_review(review_text):
            instance.ai_checked_status = "ai_cancelled"
            instance.is_published = False
        else:
            instance.ai_checked_status = "ai_checked_true"
            instance.is_published = True

        instance.save()

# @receiver(post_save, sender=Order)
# def telegram_order_notify(sender, instance, created, **kwargs):
#     # Created - это флаг, который показывает, что запись была создана
#     if created:
#         # Формируем сообщение в MD разметке
#         # time_zone = pytz.timezone('Europe/Moscow') 
#         localized_time = instance.date_created.astimezone(time_zone)
#         formatted_time = localized_time.strftime('%d.%m.%Y %H:%M')
#         message = f"""
#         ** Новый заказ {formatted_time} **
#         Имя клиента: {instance.client_name}
#         Телефон: {instance.phone}
#         Мастер: {instance.master.name}
#         ---
#         Комментарий: {instance.comment}
#         ---
#         Админ-панель: http://127.0.0.1:8000/admin/core/order/{instance.id}/change/
#         #заказ #{instance.master.name}
#         """
#         # Отправляем сообщение в телеграм
#         asyncio.run(send_telegram_message(TELEGRAM_BOT_API_KEY, TELEGRAM_USER_ID, message))

@receiver(m2m_changed, sender=Order.services.through)
def telegram_order_notify(sender, instance, action, **kwargs):
    """
    Обработчик сигнала m2m_changed для модели Order.
    Отправляет уведомление только при создании НОВОГО заказа с услугами.
    """

    if action == 'post_add' and kwargs.get('pk_set') and timezone.now() - instance.date_created < timedelta(seconds=5):
        # Получаем список услуг
        # time_zone = pytz.timezone('Europe/Moscow') 
        services = [service.name for service in instance.services.all()]
        localized_time = instance.date_created.astimezone(time_zone)
        formatted_time = localized_time.strftime('%d.%m.%Y %H:%M')

        # Формируем сообщение в MD разметке
        message = (
                f"**Новый заказ {formatted_time}**\n"
                f"Имя: {instance.client_name}\n"
                f"Телефон: {instance.phone}\n"
                f"Мастер: {instance.master.name}\n"
                f"Услуги: {', '.join(services) or 'Не указано'}\n"
                "---\n"
                f"Комментарий: {instance.comment or 'Не указан'}\n"
                f"Админ-панель: http://127.0.0.1:8000/admin/core/order/{instance.id}/change/"
                f"#заказ #{instance.master.name}"
            )
        # Отправляем сообщение в телеграм
        asyncio.run(send_telegram_message(TELEGRAM_BOT_API_KEY, TELEGRAM_USER_ID, message))
