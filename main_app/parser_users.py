import asyncio
import os.path
import sys
from pathlib import Path

from asgiref.sync import sync_to_async, async_to_sync
from telethon import TelegramClient
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch, Channel, UserStatusOnline, UserStatusOffline
from django.utils import timezone
from .models import TelegramUser  # замените на правильный импорт
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
from ProjectsTemplate import settings

api_id = 28632508
api_hash = '6d260b5e6e9a606f44a38fc43bbe8bbc'
phone = '+380999491488'


@sync_to_async
def save_user_to_db(user, chat_id, image_filename, last_seen):
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
            'scraped_at': timezone.now(),
            'image': image_filename,
            'last_seen': last_seen
        }
    )
    return created


def get_client():
    return TelegramClient('session_name1', api_id, api_hash)


async def collect_users_by_chat_id(chat_id):
    client = get_client()
    async with client:
        await client.start(phone)
        print("📡 Подключение к Telegram...")

        # Получаем сущность и проверяем, что это именно группа или канал
        try:
            entity = await client.get_entity(chat_id)
        except Exception as e:
            print(f"❌ Не удалось получить сущность по chat_id: {e}")
            return

        if not isinstance(entity, Channel):
            print("❌ Это не группа/канал, а, скорее всего, пользователь. Остановка.")
            return

        # Получаем InputChannel
        input_channel = await client.get_input_entity(entity)

        limit = 50
        offset = 0
        all_users = []

        while True:
            participants = await client(GetParticipantsRequest(
                channel=input_channel,
                filter=ChannelParticipantsSearch(''),
                offset=offset,
                limit=limit,
                hash=0
            ))

            if not participants.users:
                break

            all_users.extend(participants.users)
            print(f"Загружено пользователей: {len(all_users)}")

            for user in participants.users:
                image_filename = None
                try:
                    photo_path = await client.download_profile_photo(
                        user,
                        file=os.path.join(settings.MEDIA_ROOT, 'img', 'users', f'{user.id}.jpg')
                    )
                    if photo_path:
                        image_filename = f"img/users/{user.id}.jpg"
                except Exception as e:
                    print(f"⚠️ Не удалось скачать фото для пользователя {user.id}: {e}")

                status = user.status
                last_seen = None

                if isinstance(status, UserStatusOnline):
                    last_seen = timezone.now()
                elif isinstance(status, UserStatusOffline):
                    last_seen = status.was_online  # datetime
                elif status is not None:
                    # Для случаев UserStatusRecently, UserStatusLastWeek и др.
                    last_seen = status.__class__.__name__.replace('UserStatus', '').lower()
                else:
                    last_seen = None

                created = await save_user_to_db(user, chat_id, image_filename, last_seen)
                if created:
                    print(f"✅ Пользователь {user.id} сохранён")
                else:
                    print(f"⚠️ Пользователь {user.id} уже есть")

            offset += limit

        print(f"🎉 Обработка пользователей завершена. Всего: {len(all_users)}")


def create_users_sync(chat_id):
    return async_to_sync(collect_users_by_chat_id)(chat_id)
