import asyncio
import os
import time
from pprint import pprint

from asgiref.sync import sync_to_async, async_to_sync
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, MessageMediaPhoto
from telethon.tl.functions.messages import GetHistoryRequest
from .models import Post  # Замените на правильный путь к вашей модели
from django.utils import timezone

api_id = 28632508
api_hash = '6d260b5e6e9a606f44a38fc43bbe8bbc'
phone = '+380999491488'

client = TelegramClient('session_name', api_id, api_hash)

async def start_client():
    await client.start(phone)
    print("Telegram client started")

# Гарантируем, что клиент стартован, и можно ждать вызова
loop = asyncio.get_event_loop()
async def get_all_groups_dict():
    async with TelegramClient('session_name1', api_id, api_hash) as client:
        await client.start(phone)
        result = await client(GetDialogsRequest(
            offset_date=None,
            offset_id=0,
            offset_peer=InputPeerEmpty(),
            limit=200,
            hash=0
        ))
        groups = [chat for chat in result.chats if getattr(chat, 'megagroup', False)]
        return [(g.id, g.title) for g in groups]

@sync_to_async
def save_post(post):
    post.save()

async def collect_posts_by_chat_id(chat_id, target_user_id, page=1, page_size=100):
    async with TelegramClient('session_name1', api_id, api_hash) as client:
        print("📡 Подключение к Telegram...")

        dialogs = await client(GetDialogsRequest(
            offset_date=None,
            offset_id=0,
            offset_peer=InputPeerEmpty(),
            limit=200,
            hash=0
        ))

        groups = dialogs.chats
        target_group = next((g for g in groups if g.id == chat_id), None)

        if not target_group:
            print("❌ Группа с таким chat_id не найдена.")
            return

        print(f"\n📥 Парсинг сообщений из: {target_group.title}")

        matched_messages = []
        offset_id = 0
        messages_to_skip = (page - 1) * page_size
        messages_collected = 0

        while True:
            history = await client(GetHistoryRequest(
                peer=target_group,
                offset_id=offset_id,
                limit=100,
                max_id=0,
                min_id=0,
                add_offset=0,
                offset_date=None,
                hash=0
            ))

            if not history.messages:
                break

            for msg in history.messages:
                offset_id = msg.id  # Обновляем даже если не подошёл

                if getattr(msg, 'sender_id', None) != target_user_id or not hasattr(msg, 'message'):
                    continue

                if messages_to_skip > 0:
                    messages_to_skip -= 1
                    continue

                matched_messages.append(msg)
                messages_collected += 1

                if messages_collected >= page_size:
                    break

            print(f"🔎 Отобрано {messages_collected} сообщений пользователя {target_user_id}")
            if messages_collected >= page_size:
                break

            await asyncio.sleep(1)

        for message in matched_messages:
            text = message.message.replace("\n", " ").replace("\r", "") if message.message else None

            if isinstance(message.media, MessageMediaPhoto):
                photo_filename = f"photo_{message.id}.jpg"
                photo_path = await client.download_media(
                    message.media,
                    file=os.path.join(os.getcwd(), 'static', 'img', photo_filename)
                )
                photo = photo_filename
            else:
                photo = "No photo"

            date_str = timezone.localtime(message.date)

            post, created = await Post.objects.aget_or_create(
                sender_id=str(message.sender_id),
                chat_id=target_group.id,
                text=text,
                defaults={
                    'date': date_str,
                    'photo': photo,
                    'comment_count': 'Not Available'
                }
            )

            if created:
                print(f"✅ Пост {message.id} сохранён.")
            else:
                print(f"⚠️ Пост {message.id} уже существует, пропущен.")

        print(f"🎉 Завершено. Загружено {len(matched_messages)} сообщений для страницы {page}.")

def get_groups_sync():
    # Вызываем async функцию синхронно
    return async_to_sync(get_all_groups_dict)()

def create_posts_sync(chat_id, user_id, page):
    # Вызываем async функцию синхронно
    return async_to_sync(collect_posts_by_chat_id)(chat_id, user_id, page, 100)