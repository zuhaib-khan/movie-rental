from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("/account", views.index, name="account"),
    path("/movie", views.index, name="movie"),
    path("/rent", views.index, name="rent"),
    path("/dbUser", views.index, name="dbUser"),
    path("/dbMovie", views.index, name="dbMovie"),
    path("/dbRent", views.index, name="dbRent"),
]