import os
import django
import asyncio

from asgiref.sync import sync_to_async
from django.utils import timezone
from django.utils.timezone import now
from datetime import datetime

# ✅ Подключаем Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ProjectsTemplate.settings')  # 🔁 замени на свой проект
django.setup()

# 📦 Импортируем модель и Telethon
from main_app.models import ScheduledMessage
from telethon import TelegramClient

# 🔑 Данные авторизации Telegram
api_id = 28632508
api_hash = '6d260b5e6e9a606f44a38fc43bbe8bbc'

@sync_to_async
def get_scheduled_messages():
    return list(ScheduledMessage.objects.filter(is_sent=False, scheduled_time__lte=now()))

@sync_to_async
def mark_as_sent(message):
    message.is_sent = True
    message.save()


# 📤 Отправка отложенных сообщений
async def send_scheduled_messages():
    async with TelegramClient('scheduler_session', api_id, api_hash) as client:
        while True:
            messages = await get_scheduled_messages()
            for msg in messages:
                try:
                    if timezone.now() >= msg.scheduled_time:
                        # await client.send_message(msg.chat_id, msg.message_text)
                        await mark_as_sent(msg)
                        print(f"[{datetime.now()}] ✅ Отправлено в {msg.chat_id}: {msg.message_text[:30]}")
                except Exception as e:
                    print(f"[{datetime.now()}] ❌ Ошибка: {e}")
            await asyncio.sleep(30)

# 🚀 Точка входа
if __name__ == '__main__':
    asyncio.run(send_scheduled_messages())