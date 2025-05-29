import asyncio
import threading
import time
import urllib
from pprint import pprint
from urllib.parse import unquote

from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from asgiref.sync import async_to_sync, sync_to_async
from django.urls import reverse

from .models import Post, TelegramUser, ScheduledMessage

from .forms import LoginForm, SignupForm, SimpleScheduleForm  # ✅ лучше и понятнее
from .parser_posts import join_and_get_info_sync, create_posts_sync, create_posts_from_group_sync
from .parser_users import create_users_sync
from .parse_groups import get_group_titles

async def index(request):
    chat_ids = await sync_to_async(list)(TelegramUser.objects.values_list('chat_id', flat=True).distinct())
    try:
        groups = await get_group_titles(chat_ids)
    except Exception:
        groups = {}
    pprint(groups)
    return render(request, 'index.html', {'groups': groups})



def get_group_users_info(request, chat_id, title, page=1):
    try:
        page = int(page)
        chat_id = int(chat_id)

        start = (page - 1) * 50
        end = page * 50

        users = TelegramUser.objects.filter(chat_id=chat_id)[start:end]
        users_dict = {}
        r = 1
        for user in users:
            users_dict[r] = (user, len(Post.objects.filter(chat_id=chat_id, sender_id=user.telegram_id)))
            r += 1
        has_next = len(users) == 50
        has_previous = page > 1

        title = unquote(title)

        return render(request, 'users_list.html', context={
            'users': users_dict,
            'current_page': page,
            'next_page': page + 1 if has_next else None,
            'previous_page': page - 1 if has_previous else None,
            'chat_id': chat_id,
            'title': title
        })
    except Exception as e:
        print(e)
        return redirect('error')


def get_group_banned_users_info(request, chat_id, title, page=1):
    try:
        page = int(page)
        chat_id = int(chat_id)

        start = (page - 1) * 50
        end = page * 50

        users = TelegramUser.objects.filter(chat_id=chat_id, is_banned=True)[start:end]
        users_dict = {}
        r = 1
        for user in users:
            users_dict[r] = (user, len(Post.objects.filter(chat_id=chat_id, sender_id=user.telegram_id)))
            r += 1
        has_next = len(users) == 50
        has_previous = page > 1

        title = unquote(title)

        return render(request, 'users_list.html', context={
            'users': users_dict,
            'current_page': page,
            'next_page': page + 1 if has_next else None,
            'previous_page': page - 1 if has_previous else None,
            'chat_id': chat_id,
            'title': title
        })
    except Exception as e:
        print(e)
        return redirect('error')

def get_group_active_users_info(request, chat_id, title, page=1):
    try:
        page = int(page)
        chat_id = int(chat_id)

        start = (page - 1) * 50
        end = page * 50

        users = TelegramUser.objects.filter(chat_id=chat_id, is_banned=False)[start:end]
        users_dict = {}
        r = 1
        for user in users:
            users_dict[r] = (user, len(Post.objects.filter(chat_id=chat_id, sender_id=user.telegram_id)))
            r += 1
        has_next = len(users) == 50
        has_previous = page > 1

        title = unquote(title)

        return render(request, 'users_list.html', context={
            'users': users_dict,
            'current_page': page,
            'next_page': page + 1 if has_next else None,
            'previous_page': page - 1 if has_previous else None,
            'chat_id': chat_id,
            'title': title
        })
    except Exception as e:
        print(e)
        return redirect('error')


def ban_user(request, chat_id, user_id):
    chat_id = int(chat_id)
    user_id = int(user_id)
    user = TelegramUser.objects.filter(telegram_id=user_id, chat_id=chat_id).first()
    user.is_banned = True
    user.save()
    return redirect("user_msgs", chat_id=chat_id, user_id=user_id, page=1)

def unban_user(request, chat_id, user_id):
    chat_id = int(chat_id)
    user_id = int(user_id)
    user = TelegramUser.objects.filter(telegram_id=user_id, chat_id=chat_id).first()
    user.is_banned = False
    user.save()
    return redirect("user_msgs", chat_id=chat_id, user_id=user_id, page=1)

def user_msgs(request, chat_id, user_id, page=1):
    try:
        page = int(page)
        chat_id = int(chat_id)
        user_id = int(user_id)

        start = (page - 1) * 50
        end = page * 50

        posts = Post.objects.filter(sender_id=user_id, chat_id=chat_id).order_by('id')[start:end]

        has_next = len(posts) == 50
        has_previous = page > 1

        user = TelegramUser.objects.filter(telegram_id=user_id, chat_id=chat_id).first()

        return render(request, 'user_detail.html', {
            'posts': posts,
            'user': user,
            'current_page': page,
            'next_page': page + 1 if has_next else None,
            'previous_page': page - 1 if has_previous else None,
            'user_id': user_id,
            'chat_id': chat_id
        })
    except Exception as e:
        print(e)
        return redirect('error')

def error_page(request):
    return render(request, 'error.html')






def get_group_posts(request, chat_id, title, page=1):
    page = int(page)
    chat_id = int(chat_id)

    # Получаем текст из формы поиска, если он есть (POST)
    search_word = None
    if request.method == 'POST':
        search_word = request.POST.get('search_word', '').strip()

    # Фильтруем посты по chat_id
    posts_query = Post.objects.filter(chat_id=chat_id)

    # Если есть поисковый запрос, добавляем фильтр по тексту (поле "text" - замени на своё, если другое)
    if search_word:
        posts_query = posts_query.filter(text__icontains=search_word)

    # Сортируем и берем срез для пагинации
    start = (page - 1) * 100
    end = page * 100
    posts_page = posts_query.order_by('id')[start:end]

    # Формируем словарь пост: пользователь
    posts = {post: TelegramUser.objects.filter(telegram_id=post.sender_id).first() for post in posts_page}

    has_next = len(posts) == 100
    has_previous = page > 1

    title = unquote(title)
    return render(request, 'posts_list.html', context={
        'has_previous': has_previous,
        'has_next': has_next,
        'current_page': page,
        'title': title,
        'posts': posts,
        'chat_id': chat_id,
        'next_page': page + 1 if has_next else None,
        'previous_page': page - 1 if has_previous else None,
        'search_word': search_word,  # чтобы можно было вернуть в форму, если нужно
    })

def parse_index(request):
    try:
        if request.method == 'POST':
            group_link = request.POST.get('group_link')
            try:
                if group_link:
                    chat_id, title = join_and_get_info_sync(group_link)
                    if not chat_id:
                        messages.error(request, "Не удалось вступить в чат!")  # 👈 передаём сообщение
                        return redirect('index')
                    print(chat_id)
                    url = reverse('parse_group_info_full', kwargs={'chat_id': chat_id})
                    return redirect(url)

                # Если group_link пустой, просто снова показываем форму
                return render(request, 'parse_index.html')
            except Exception:
                return redirect('error')

        # Для GET запроса просто показываем форму (input)
        return render(request, 'parse_index.html')
    except Exception as e:
        print(e)
        return redirect('error')
_parsing_lock = threading.Lock()

def run_parsing(chat_id):
    with _parsing_lock:
        create_users_sync(chat_id)
        create_posts_from_group_sync(chat_id)


def parse_group_info_full(request, chat_id):
    chat_id = int(f'-100{chat_id}')
    thread = threading.Thread(target=run_parsing, args=(chat_id,))
    thread.daemon = True
    thread.start()
    return redirect('index')

def get_scheduled_msgs(request, chat_id, title, page=1):
    page = int(page)
    chat_id = int(chat_id)
    start = (page - 1) * 50
    end = page * 50
    scheduled_msgs = ScheduledMessage.objects.filter(chat_id=chat_id).order_by('-id')[start:end]
    has_next = len(scheduled_msgs) == 100
    has_previous = page > 1
    return render(request, 'scheduled_msgs.html', context={
        'has_previous': has_previous,
        'has_next': has_next,
        'current_page': page,
        'title': title,
        'messages': scheduled_msgs,
        'chat_id': chat_id,
        'next_page': page + 1 if has_next else None,
        'previous_page': page - 1 if has_previous else None,
    })

def create_scheduled_msgs(request, chat_id, title):
    chat_id = int(chat_id)  # Преобразуем chat_id в целое число
    if request.method == 'POST':
        form = SimpleScheduleForm(request.POST)
        if form.is_valid():
            message = form.cleaned_data['message']
            scheduled_time = form.cleaned_data['scheduled_time']

            print(f'Chat ID: {chat_id}')
            print(f'Message: {message}')
            print(f'Scheduled Time: {scheduled_time}')
            ScheduledMessage.objects.get_or_create(
                chat_id=chat_id,
                message_text=message,
                scheduled_time=scheduled_time,
            )

            return redirect('get_scheduled_msgs', chat_id=str(chat_id), title=title, page=1)
    else:
        form = SimpleScheduleForm()

    return render(request, 'create_scheduled.html', context={
        'title': title,
        'chat_id': chat_id,
        'form': form
    })

# from django.contrib.auth import authenticate, login
# from django.shortcuts import redirect

# def login_page(request):
#     form = LoginForm(request.POST or None)
#     if request.method == 'POST' and form.is_valid():
#         username = form.cleaned_data['login']
#         password = form.cleaned_data['password']
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect('index')  # или куда-то ещё
#         else:
#             form.add_error(None, 'Invalid username or password.')
#     return render(request, 'account/login.html', {'form': form})
#
#
# def register_page(request):
#     form = SignupForm(request.POST or None)
#     if request.method == 'POST' and form.is_valid():
#         user = form.save()  # Сохраняет пользователя (если форма наследует от UserCreationForm)
#         login(request, user)  # Автоматически логинит после регистрации
#         return redirect('index')  # Перенаправление после успешной регистрации
#     return render(request, 'account/signup.html', {'form': form})