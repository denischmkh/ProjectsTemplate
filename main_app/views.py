import asyncio

from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from asgiref.sync import async_to_sync
from .models import Post, TelegramUser

from .forms import LoginForm, SignupForm  # ✅ лучше и понятнее
from .parser_posts import get_groups_sync, create_posts_sync
from .parser_users import create_users_sync

def index(request):
    groups = get_groups_sync()
    return render(request, 'index.html', context={'groups': groups})


def item_list(request, chat_id: int, page=1):
    start = (page-1)*50
    end = page*50
    create_users_sync(chat_id=chat_id, page=page)
    users = TelegramUser.objects.filter(chat_id=chat_id)[start:end]
    if len(users) < 50:
        has_next = False
    else:
        has_next = True

    if page > 1:
        has_previous = True
    else:
        has_previous = False

    return render(request, 'item_list.html', context={
                                                      'users': users,
                                                      'current_page': page,
                                                      'next_page': page+1 if has_next else None,
                                                      'previous_page': page-1 if has_previous else None,
                                                      'chat_id': chat_id})


def item_detail(request, chat_id, user_id):

    return render(request, 'item_detail.html')

from django.contrib.auth import authenticate, login
from django.shortcuts import redirect

def login_page(request):
    form = LoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        username = form.cleaned_data['login']
        password = form.cleaned_data['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')  # или куда-то ещё
        else:
            form.add_error(None, 'Invalid username or password.')
    return render(request, 'account/login.html', {'form': form})


def register_page(request):
    form = SignupForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()  # Сохраняет пользователя (если форма наследует от UserCreationForm)
        login(request, user)  # Автоматически логинит после регистрации
        return redirect('index')  # Перенаправление после успешной регистрации
    return render(request, 'account/signup.html', {'form': form})