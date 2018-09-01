from django.urls import path

from .views import get_or_create_posts, get_update_or_delete_post_by_id, get_update_or_delete_post_by_slug

urlpatterns = [
    path('', get_or_create_posts),
    path('<int:post_id>/', get_update_or_delete_post_by_id),
    path('<str:slug>/', get_update_or_delete_post_by_slug),
]
