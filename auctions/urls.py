from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('create', views.create, name="create"),
    path('listing/<int:listing_id>', views.listing, name="listing"),
    path('unwatch/<int:listing_id>', views.unwatch, name="unwatch"),
    path('watch/<int:listing_id>', views.watch, name="watch"),
    path('watchlist', views.watchlist, name="watchlist"),
    path('bid/<int:listing_id>', views.bid, name="bid"),
    path('close/<int:listing_id>', views.close, name="close"),
    path('categories', views.categories, name="categories")
]
