from django.shortcuts import render
from django.http import HttpResponse
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.forms import ModelForm
from django.forms.models import model_to_dict

from .models import Customer, Rentals, Movies


def index(request):
    return render(request, "app/index.html")


def account(request):
    if request.method == "POST":

        email_id=request.POST["email_id"]
        first_name=request.POST["first_name"]
        last_name=request.POST["last_name"]
        
        if Customer.objects.filter(pk=email_id).exists():
        # Customer already present, failure
            # Customer.objects.get(pk=email_id)
            return render(request, "app/account.html", {"form": NewAccountForm(), "status": -1})
        else:
        # Add the new customer to the db, success
            customer = Customer(email_id=email_id, first_name=first_name, last_name=last_name)
            customer.save()
            return render(request, "app/account.html", {"form": NewAccountForm(), "status": 1})
    
    return render(request, "app/account.html", {"form": NewAccountForm()})


def movie(request):
    movies = Movies.objects.all()
    
    prefilled_movie_forms = []
    for movie in movies:
        prefilled_movie_forms.append(MoviesForm(model_to_dict(movie)))
    
    if request.method == "POST":

        title=request.POST["title"]
        
        if Movies.objects.filter(pk=title).exists():
        # Movie already present, failure
            return render(request, "app/movie.html", {"form": NewMovieForm(), "movies_form": prefilled_movie_forms, "movie_list": movies, "status": -1})
        else:
        # Add the new movie to the db, success
            movie = Movies(title=title)
            movie.save()
            return render(request, "app/movie.html", {"form": NewMovieForm(),  "movies_form": prefilled_movie_forms, "movie_list": movies})
    return render(request, "app/movie.html", {"form": NewMovieForm(),  "movies_form": prefilled_movie_forms, "movie_list": movies})


def rent(request):
    return HttpResponse("Placeholder for now.")

def db_user(request):
    return HttpResponse("Placeholder for now.")


def db_movie(request):
    title = request.POST["title"]
    print("mmm", title)
    quantity = request.POST["quantity"]
    Movies(title=title, quantity=quantity).save()
    return HttpResponseRedirect(reverse("app:movie"))


def db_rent(request):
    return HttpResponse("Placeholder for now.")


class NewAccountForm(forms.Form): # Form for creating a new account
    email_id = forms.EmailField(label="Email ID")
    first_name = forms.CharField(label="First Name")
    last_name = forms.CharField(label="Last Name")
    
class NewMovieForm(forms.Form): # Form for creating a new movie
    title = forms.CharField(label="Title")

class MoviesForm(ModelForm):
    class Meta:
        model = Movies
        fields = '__all__'