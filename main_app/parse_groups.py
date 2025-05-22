from asgiref.sync import async_to_sync
from django.shortcuts import render
from .models import TelegramUser
from telethon import TelegramClient
import asyncio

api_id = 28632508
api_hash = '6d260b5e6e9a606f44a38fc43bbe8bbc'
phone = '+380999491488'

async def get_chat_title(client, chat_id):
    try:
        entity = await client.get_entity(chat_id)
        title = getattr(entity, 'title', None)
        return chat_id, title
    except Exception as e:
        # Если чат не найден или ошибка — возвращаем None
        return chat_id, None

async def get_all_group_titles(chat_ids):
    async with TelegramClient('session_name1', api_id, api_hash) as client:
        tasks = [get_chat_title(client, chat_id) for chat_id in chat_ids]
        results = await asyncio.gather(*tasks)
        return dict(results)

async def get_group_titles(chat_ids):
    return await get_all_group_titles(chat_ids)
