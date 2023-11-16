from collections.abc import Iterable
from django.db import models
from django.contrib.auth.models import UserManager
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin

# Create your models here.

class SneakerUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("El email es obligatorio")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_user(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_admin", False)
        return self._create_user(email, password, **extra_fields)
    
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_admin", True)
        return self._create_user(email, password, **extra_fields)
    
class SneakerUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name='email', max_length=60, unique=True)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email' 
    REQUIRED_FIELDS = [] 
    objects = SneakerUserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-date_joined']
    
    

class Customer(models.Model):
    user = models.OneToOneField(SneakerUser, null=True, blank=True, on_delete = models.CASCADE)
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
    
    class Meta:
        verbose_name = 'Status'
        verbose_name_plural = 'Status'
        ordering = ['name']

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

    class Meta:
        verbose_name = 'Shipping address'
        verbose_name_plural = 'Shipping addresses'
        ordering = ['-date_added']


