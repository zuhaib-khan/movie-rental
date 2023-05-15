from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def account(request):
    return HttpResponse("Placeholder for now.")


def movie(request):
    return HttpResponse("Placeholder for now.")


def rent(request):
    return HttpResponse("Placeholder for now.")

def db_user(request):
    return HttpResponse("Placeholder for now.")


def db_movie(request):
    return HttpResponse("Placeholder for now.")


def db_rent(request):
    return HttpResponse("Placeholder for now.")