
from django.urls import path

from . import views

app_name = "store"
urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("clients", views.clients, name="clients"),
    path("categories", views.categories, name="categories"),
    path("category/<str:name>", views.category, name="category"),
    path("course/<int:course_id>", views.course, name="course"),
    path('profile', views.profile, name="profile"),
    path('search', views.search, name="search"),
    path('addItem', views.addItem, name="addItem"),
    path('removeItem', views.removeItem, name="removeItem"),
    path('cart', views.cart, name="cart"),
    path('payment', views.payment, name="payment"),
]
