from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete = models.CASCADE)
    name = models.CharField(max_length=200 , null=True)
    email = models.CharField(max_length=200 , null=True)

    def __str__(self):
        return self.name

class Brand(models.Model):
    name = models.CharField(max_length=200 , null=False, unique=True, blank=False)
    
    def __str__(self):
        return self.name
   
class Product(models.Model):
    name = models.CharField(max_length=200 , null=True)
    price = models.FloatField()
    brand = models.ForeignKey(Brand, null=True, on_delete = models.SET_NULL)
    image = models.ImageField(null=True, blank=True)
    
    def __str__(self):
        return self.name
    
class Status(models.Model):
    name = models.CharField(max_length=200 , null=False, unique=True, blank=False)
    
    def __str__(self):
        return self.name

class Order(models.Model):
    customer = models.ForeignKey(Customer, null=True, on_delete = models.SET_NULL)
    date_ordered = models.DateTimeField(auto_now_add=True)
    status = models.ForeignKey(Status, null=True, on_delete = models.SET_NULL)

    def __str__(self):
        return str(self.id)
    
class OrderItem(models.Model):
    product = models.ForeignKey(Product, null=True, on_delete = models.SET_NULL)
    order = models.ForeignKey(Order, null=True, on_delete = models.SET_NULL)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, null=True, on_delete = models.SET_NULL)
    order = models.ForeignKey(Order, null=True, on_delete = models.SET_NULL)
    address = models.CharField(max_length=200 , null=True)
    city = models.CharField(max_length=200 , null=True)
    state = models.CharField(max_length=200 , null=True)
    zipcode = models.CharField(max_length=200 , null=True)
    coutry = models.CharField(max_length=200 , null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.address


