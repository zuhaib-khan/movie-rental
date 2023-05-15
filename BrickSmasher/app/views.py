from django.shortcuts import render
from django.http import HttpResponse
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect

from .models import Customer, Rentals, Movies


def index(request):
    return render(request, "app/index.html")


def account(request):
    if request.method == "POST":

        email_id=request.POST["email_id"]
        first_name=request.POST["first_name"]
        last_name=request.POST["last_name"]

        # Add the new customer to the db
        c = Customer(email_id=email_id, first_name=first_name, last_name=last_name)
        c.save()

        # Redirect user to Home
        return HttpResponseRedirect(reverse("app:index"))


    return render(request, "app/account.html", {"form": NewAccountForm()})


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


class NewAccountForm(forms.Form): # Form for creating a new account
    email_id = forms.EmailField(label="Email ID")
    first_name = forms.CharField(label="First Name")
    last_name = forms.CharField(label="Last Name")