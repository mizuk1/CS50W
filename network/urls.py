
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("compose", views.compose, name="compose"),
    path("profile/<str:username>", views.profile, name="profile"),
    path('following', views.following, name="following"),
    path('edit/<int:post_id>', views.edit, name="edit"),
    path('like/<int:post_id>', views.like, name="like"),
    path('add_like/<int:post_id>', views.add_like, name="add_like"),
    path('rem_like/<int:post_id>', views.remove_like, name="remove_like"),
]
