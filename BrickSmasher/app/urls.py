from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("account", views.account, name="account"),
    path("movie", views.movie, name="movie"),
    path("rent", views.rent, name="rent"),
    path("dbUser", views.db_user, name="db_user"),
    path("dbMovie", views.db_movie, name="db_movie"),
    path("dbRent", views.db_rent, name="db_rent"),
]