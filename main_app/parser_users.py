import asyncio
from asgiref.sync import sync_to_async, async_to_sync
from telethon import TelegramClient
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch
from django.utils import timezone
from .models import TelegramUser  # замените на правильный импорт

api_id = 28632508
api_hash = '6d260b5e6e9a606f44a38fc43bbe8bbc'
phone = '+380999491488'

@sync_to_async
def save_user_to_db(user, chat_id):
    obj, created = TelegramUser.objects.update_or_create(
        telegram_id=user.id,
        chat_id=chat_id,
        defaults={
            'username': getattr(user, 'username', None),
            'first_name': getattr(user, 'first_name', None),
            'last_name': getattr(user, 'last_name', None),
            'phone': getattr(user, 'phone', None),
            'is_bot': getattr(user, 'bot', False),
            'is_restricted': getattr(user, 'restricted', None),
            'is_fake': getattr(user, 'fake', None),
            'is_scam': getattr(user, 'scam', None),
            'is_premium': getattr(user, 'premium', None),
            'scraped_at': timezone.now()
        }
    )
    return created

def get_client():
    return TelegramClient('session_name1', api_id, api_hash)

async def collect_users_by_chat_id(chat_id, page):
    client = get_client()
    async with client:
        await client.start(phone)
        print("📡 Подключение к Telegram...")

        limit = 50
        offset = (page - 1) * limit
        all_users = []

        participants = await client(GetParticipantsRequest(
            channel=chat_id,
            filter=ChannelParticipantsSearch(''),
            offset=offset,
            limit=limit,
            hash=0
        ))

        if not participants.users:
            return

        all_users.extend(participants.users)
        print(f"Загружено пользователей: {len(all_users)}")

        for user in participants.users:
            created = await save_user_to_db(user, chat_id)
            if created:
                print(f"✅ Пользователь {user.id} сохранён")
            else:
                print(f"⚠️ Пользователь {user.id} уже есть")

        print(f"🎉 Обработка пользователей завершена. Всего: {len(all_users)}")

def create_users_sync(chat_id, page=1):
    return async_to_sync(collect_users_by_chat_id)(chat_id, page)