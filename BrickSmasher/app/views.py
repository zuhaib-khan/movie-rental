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
    form = CustomerForm()
    return render(request, 'app/account.html', {'form': form})


def movie(request):
    return render(request, "app/movie.html")


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


@csrf_exempt
def db_user(request):
    if request.method == 'GET':
        email_id = request.GET.get('email_id')
        customer = Customer.objects.filter(email_id=email_id).values('first_name', 'last_name').first()
        return JsonResponse(customer)
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email_id = request.POST.get('email_id')
        if Customer.objects.filter(email_id=email_id).exists():
            return JsonResponse({'error': 'Email already exists!'}, status=400)
        else:
            customer = Customer(first_name=first_name, last_name=last_name, email_id=email_id)
            customer.save()
            return JsonResponse({'message': 'Account created successfully!'}, status=201)


@csrf_exempt
def db_movie(request):
    if request.method == 'GET':
        movies = list(Movies.objects.order_by('title').values())
        return JsonResponse({'movies': movies})
    elif request.method == 'POST':
        action = request.POST.get('action')
        title = request.POST.get('title').strip()
        if action == 'new':
            if Movies.objects.filter(title=title).exists():
                return JsonResponse({'status': 'error', 'error': 'title_exists'})
            else:
                movie = Movies(title=title, quantity=1)
                movie.save()
                return JsonResponse({'status': 'success'})
        elif action in ['add', 'remove']:
            movie = Movies.objects.get(title=title)
            if action == 'add':
                movie.quantity += 1
            else:
                if movie.quantity > 0:
                    movie.quantity -= 1
            movie.save()
            return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})


@csrf_exempt
def db_rent(request):
    if request.method == 'GET':
        email_id = request.GET.get('email_id')
        rentals = list(Rentals.objects.filter(email_id_id=email_id).values())
        return JsonResponse({"rentals": rentals})
        
    if request.method == 'POST':
        data = json.loads(request.body)
        title = data.get('title')
        email_id = data.get("email_id")
        customer = Customer.objects.get(email_id=email_id)
        movie = Movies.objects.get(title=title)
        Rentals(email_id=customer, title=movie).save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
    
class NewMovieForm(forms.Form): # Form for creating a new movie
    title = forms.CharField(label="Title")
    
class RetrieveRentalsForm(forms.Form):
    email_id = forms.EmailField(label="Email ID")