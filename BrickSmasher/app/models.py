from django.db import models

# Create your models here.

class Customer(models.Model):
    email_id = models.EmailField(primary_key=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    

class Movies(models.Model):
    title = models.CharField(primary_key=True)
    quantity = models.IntegerField()


class Rentals(models.Model):
    email_id = models.ForeignKey(Customer, primary_key=True)
    title = models.ForeignKey(Movies, primary_key=True)
    