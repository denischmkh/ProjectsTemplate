"""
URL configuration for ProjectsTemplate project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import os
import sys

from django.contrib import admin
from django.urls import path, re_path

sys.path.append(os.path.join(os.getcwd(), '..'))
from main_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),

    # Разрешаем отрицательные chat_id через re_path
    re_path(r'^users/group/(?P<chat_id>-?\d+)/(?P<title>[^/]+)/(?P<page>\d+)$', views.get_group_users_info, name='get_group_users'),
    re_path(r'^users/profile/(?P<chat_id>-?\d+)/(?P<user_id>\d+)/(?P<page>\d+)$', views.user_msgs, name='user_msgs'),
    re_path(r'^posts/group/(?P<chat_id>-?\d+)/(?P<title>[^/]+)/(?P<page>\d+)$', views.get_group_posts, name='get_group_posts'),

    path('users/error', views.error_page, name='error'),
    path('parse/', views.parse_index, name='parse_index'),
    re_path(r'^parse/parse_group/(?P<chat_id>-?\d+)$', views.parse_group_info_full, name='parse_group_info_full'),
]

