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
from django.urls import path
sys.path.append(os.path.join(os.getcwd(), '..'))
from main_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('users/', views.users_index, name='users_index'),
    path('users/parse_group/<int:chat_id>/<str:title>/<int:page>', views.parse_group_users_info, name='parse_group_info'),
    path('users/group/<int:chat_id>/<str:title>/<int:page>', views.get_group_users_info, name='get_group_info'),
    path('users/profile/<int:chat_id>/<int:user_id>/<int:page>', views.user_msgs, name='user_msgs'),
    path('users/error', views.error_page, name='error'),

    path('posts/', views.posts_index, name='posts_index'),
    path('posts/parse_group/<int:chat_id>/<str:title>/<int:page>', views.parse_group_posts, name='parse_group_posts'),
    path('posts/group/<int:chat_id>/<str:title>/<int:page>', views.get_group_posts, name='get_group_posts'),
]

