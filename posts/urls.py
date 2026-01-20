from django.urls import path
from . import views

urlpatterns = [
    path("users/", views.list_users, name="list_users"),
    path("users/create/", views.create_user, name="create_user"),
    path("posts/", views.list_posts, name="list_posts"),
    path("posts/create/", views.create_post, name="create_post"),
]
