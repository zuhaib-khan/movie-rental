from django.db import models

# Create your models here.

class Customer(models.Model):
    email_id = models.EmailField(primary_key=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    

class Movies(models.Model):
    title = models.CharField(primary_key=True, max_length=60)
    quantity = models.IntegerField()


class Rentals(models.Model):
    email_id = models.ManyToManyField(Customer)
    title = models.ManyToManyField(Movies)
    