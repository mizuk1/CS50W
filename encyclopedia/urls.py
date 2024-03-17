from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:title>", views.title, name="title"),
    path("create/", views.create, name="create"),
    path("edit/<str:title>/", views.edit, name="edit"),
    path("random/", views.random_entry, name="random_entry")
]
