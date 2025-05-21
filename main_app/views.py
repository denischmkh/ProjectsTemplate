import asyncio
import urllib
from urllib.parse import unquote

from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from asgiref.sync import async_to_sync
from django.urls import reverse

from .models import Post, TelegramUser

from .forms import LoginForm, SignupForm  # ✅ лучше и понятнее
from .parser_posts import join_and_get_info_sync, create_posts_sync
from .parser_users import create_users_sync

def users_index(request):
    try:
        if request.method == 'POST':
            group_link = request.POST.get('group_link')
            if group_link:
                chat_id, title = join_and_get_info_sync(group_link)
                safe_title = urllib.parse.quote(title, safe='')
                url = reverse('group_info', kwargs={'chat_id': chat_id, 'title': safe_title})
                return redirect(url)

            # Если group_link пустой, просто снова показываем форму
            return render(request, 'users_index.html')

        # Для GET запроса просто показываем форму (input)
        return render(request, 'users_index.html')
    except Exception as e:
        print(e)
        return redirect('error')


def group_users_info(request, chat_id, title, page=1):
    try:
        start = (page - 1) * 50
        end = page * 50
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
        title = unquote(title)
        return render(request, 'users_list.html', context={
            'users': users,
            'current_page': page,
            'next_page': page + 1 if has_next else None,
            'previous_page': page - 1 if has_previous else None,
            'chat_id': chat_id,
            'title': title})
    except Exception as e:
        print(e)
        return redirect('error')




def user_msgs(request, chat_id, user_id):
    try:
        create_posts_sync(chat_id=chat_id, user_id=user_id)
        posts = Post.objects.filter(sender_id=user_id, chat_id=chat_id).order_by('-date')
        user = TelegramUser.objects.filter(telegram_id=user_id).first()
        return render(request, 'user_detail.html', {'posts': posts,
                                                    'user': user})
    except Exception as e:
        print(e)
        return redirect('error')

def error_page(request):
    return render(request, 'error.html')

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