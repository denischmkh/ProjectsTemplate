import asyncio
import os
import time
from datetime import datetime
from pprint import pprint

from asgiref.sync import sync_to_async, async_to_sync
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, MessageMediaPhoto
from telethon.tl.functions.messages import GetHistoryRequest
from .models import Post  # Замените на правильный путь к вашей модели
from django.utils import timezone
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.errors import FloodWaitError, UserAlreadyParticipantError
from telethon.tl.types import PeerChannel

api_id = 28632508
api_hash = '6d260b5e6e9a606f44a38fc43bbe8bbc'
phone = '+380999491488'

client = TelegramClient('session_name', api_id, api_hash)

async def start_client():
    await client.start(phone)
    print("Telegram client started")

# Гарантируем, что клиент стартован, и можно ждать вызова
loop = asyncio.get_event_loop()


async def join_group_and_get_info(group_link_or_username):
    async with TelegramClient('session_name0', api_id, api_hash) as client:
        await client.start(phone)

        try:
            # Пробуем вступить в группу по username/link
            entity = await client.get_input_entity(group_link_or_username)
            await client(JoinChannelRequest(entity))
            print(f"✅ Вступили в группу {group_link_or_username}")
        except UserAlreadyParticipantError:
            print("Уже состоим в группе")
        except FloodWaitError as e:
            print(f"Ждем {e.seconds} секунд из-за FloodWait")
            await asyncio.sleep(e.seconds)
        except Exception as e:
            print(f"Ошибка при вступлении: {e}")
            # Можно решать, дальше ли пробовать

        # Получаем объект чата
        chat = await client.get_entity(group_link_or_username)

        # Возвращаем id и название
        return chat.id, chat.title

@sync_to_async
def save_post(msg, chat_id, target_user_id):
    text = msg.message.replace("\n", " ").replace("\r", "") if msg.message else None

    photo = "No photo"
    if isinstance(msg.media, MessageMediaPhoto):
        photo = f"photo_{msg.id}.jpg"
        # файл нужно сохранить отдельно через `await client.download_media(...)`
    dt = datetime.fromisoformat(str(timezone.localtime(msg.date)))

    # форматируем в красивый вид
    formatted = dt.strftime("%d %B %Y %H:%M:%S")

    Post.objects.get_or_create(
        date=formatted,
        sender_id=target_user_id,
        chat_id=chat_id,
        text=text,
        photo=photo,
        comment_count="Not Available"
    )

async def collect_all_user_messages(chat_id, target_user_id, max_messages=1000):
    async with TelegramClient('session_name1', api_id, api_hash) as client:
        print("📡 Подключение к Telegram...")

        async for msg in client.iter_messages(PeerChannel(chat_id), from_user=target_user_id, limit=max_messages):
            if not msg.message:
                continue

            print(f"📩 Найдено сообщение: {msg.id} — {msg.message}")

            await save_post(msg, chat_id, target_user_id)

        print(f"✅ Все сообщения от пользователя {target_user_id} сохранены.")

async def collect_all_messages_by_chat_id(chat_id):
    client = TelegramClient('session_name2', api_id, api_hash)

    async with client:
        print(f"📡 Подключение к Telegram-каналу {chat_id}...")

        count = 0
        async for msg in client.iter_messages(PeerChannel(chat_id), reverse=False, limit=4000):
            if not msg.message:
                continue

            sender_id = getattr(msg.sender_id, 'user_id', msg.sender_id)
            if sender_id is None:
                print(f"❌ Пропущено сообщение #{msg.id} — нет sender_id")
                continue
            await save_post(msg, chat_id, sender_id)
            print(f"📩 #{msg.id} — {msg.message[:50]}")
            count += 1

        print(f"✅ Всего сохранено сообщений: {count}")


def join_and_get_info_sync(group_link_or_username):
    return async_to_sync(join_group_and_get_info)(group_link_or_username)

def create_posts_sync(chat_id, user_id):
    # Вызываем async функцию синхронно
    return async_to_sync(collect_all_user_messages)(chat_id, user_id, 1000)

def create_posts_from_group_sync(chat_id):
    return async_to_sync(collect_all_messages_by_chat_id)(chat_id)