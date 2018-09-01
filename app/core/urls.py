"""typecode URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path

from app.posts.views import get_or_create_posts, get_update_or_delete_post_by_id, get_update_or_delete_post_by_slug, home

urlpatterns = [
    path('', home),
    path('admin/', admin.site.urls),
    path('api/v1/posts/', get_or_create_posts),
    path('api/v1/posts/<int:post_id>/', get_update_or_delete_post_by_id),
    path('api/v1/posts/<str:slug>/', get_update_or_delete_post_by_slug),
]