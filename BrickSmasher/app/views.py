from django.shortcuts import render
from django.http import HttpResponse
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.forms import ModelForm
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Customer, Rentals, Movies
import json


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
    movies = Movies.objects.all()
    
    all_movies = []
    for movie in movies:
        all_movies.append(model_to_dict(movie)["title"])

    if request.method == "POST":
        email_id = request.POST["email_id"]
        customer = Customer.objects.filter(pk=email_id)
        name = customer[0].first_name  + " " + customer[0].last_name
        
        # rentals =  Rentals.objects.filter(email_id=email_id).all()
        # print("lll", rentals)
        return render(request, "app/rent.html", {"form": RetrieveRentalsForm(), "email_id": email_id, "name": name, "all_movies": all_movies})

    return render(request, "app/rent.html", {"form": RetrieveRentalsForm()})
        
        
        

def db_user(request):
    return HttpResponse("Placeholder for now.")


@csrf_exempt
def db_movie(request):
    if request.method == 'POST':
        movies = json.loads(request.body)
        for title, quantity in movies.items():
            Movies(title=title, quantity=quantity).save()
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error'})


def db_rent(request):
    title = request.POST["title"]
    email_id = request.POST["email_id"]
    customer = Customer.objects.filter(pk=email_id)
    name = customer[0].first_name  + " " + customer[0].last_name
    movie = Movies(title=title)
    quantity = int(movie.quantity)
    
    if quantity < 1:
        return render(request, "app/rent.html", {"form": RetrieveRentalsForm(), "status": -1})
    
    print("lll", request.POST)
    
    # rent = Rent
    # if quantity > 0 && 


class NewAccountForm(forms.Form): # Form for creating a new account
    email_id = forms.EmailField(label="Email ID")
    first_name = forms.CharField(label="First Name")
    last_name = forms.CharField(label="Last Name")
    
class NewMovieForm(forms.Form): # Form for creating a new movie
    title = forms.CharField(label="Title")
    
class RetrieveRentalsForm(forms.Form):
    email_id = forms.EmailField(label="Email ID")

class MoviesForm(ModelForm):
    class Meta:
        model = Movies
        fields = '__all__'