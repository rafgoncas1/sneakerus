from collections.abc import Iterable
from django.db import models
from django.contrib.auth.models import UserManager
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import MinValueValidator

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
    name = models.CharField(max_length=200 , null=False, blank=False)
    email = models.EmailField(max_length=200 , null=True, blank=False)

    def __str__(self):
        return self.name

class Brand(models.Model):
    name = models.CharField(max_length=200 , null=False, unique=True, blank=False)
    
    def __str__(self):
        return self.name
   
class Color(models.Model):
    name = models.CharField(max_length=20, null=False, unique=True, blank=False)

    def __str__(self):
        return self.name

class Size(models.Model):
    name = models.FloatField(null=False, unique=True)

    def __str__(self):
        return str(self.name)


class ProductColor(models.Model):
    product = models.ForeignKey('Product', null=True, on_delete = models.SET_NULL)
    color = models.ForeignKey('Color', null=True, on_delete = models.SET_NULL)
    
    def __str__(self):
        return str(self.product) + ' ' + str(self.color)

    class Meta:
        verbose_name = 'Product color'
        verbose_name_plural = 'Product colors'
        ordering = ['product', 'color']

class ProductSize(models.Model):
    product = models.ForeignKey('Product', null=True, on_delete = models.SET_NULL)
    size = models.ForeignKey('Size', null=True, on_delete = models.SET_NULL)
    stock = models.IntegerField(default=0, null=False, blank=False, validators=[MinValueValidator(0)])
    
    def __str__(self):
        return str(self.product) + ' ' + str(self.size)

    class Meta:
        verbose_name = 'Product size'
        verbose_name_plural = 'Product sizes'
        ordering = ['product', 'size']

class Product(models.Model):
    name = models.CharField(max_length=200 , null=False, blank=False)
    price = models.DecimalField(max_digits=7, decimal_places=2, null=False, blank=False, validators=[MinValueValidator(0)])
    brand = models.ForeignKey(Brand, null=True, on_delete = models.SET_NULL)
    image = models.ImageField(null=True, blank=True)
    description = models.CharField(max_length=200 , null=True)
    details = models.CharField(max_length=200 , null=True)
    

    
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

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, null=True, on_delete = models.SET_NULL)
    address = models.CharField(max_length=200 , null=False, blank=False)
    city = models.CharField(max_length=200 , null=False, blank=False)
    state = models.CharField(max_length=200 , null=False, blank=False)
    zipcode = models.CharField(max_length=200 , null=False, blank=False)
    country = models.CharField(max_length=200 , null=False, blank=False)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.address

    class Meta:
        verbose_name = 'Shipping address'
        verbose_name_plural = 'Shipping addresses'
        ordering = ['-date_added']

class Order(models.Model):
    customer = models.ForeignKey(Customer, null=True, on_delete = models.SET_NULL)
    date_ordered = models.DateTimeField(auto_now_add=True)
    status = models.ForeignKey(Status, null=False, on_delete =models.CASCADE)
    tracking_id=models.CharField(max_length=200 , null=True, unique=True, blank=False)
    fast_delivery = models.BooleanField(default=False, null=True, blank=False)
    shipping_address = models.ForeignKey('ShippingAddress', null=True, on_delete = models.SET_NULL)

    def __str__(self):
        return str(self.id)
    
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        return sum([item.quantity for item in orderitems])

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        return sum([item.get_total for item in orderitems]) + (5 if self.fast_delivery else 0)
    
class OrderItem(models.Model):
    product_size = models.ForeignKey(ProductSize, null=True, on_delete = models.SET_NULL)
    order = models.ForeignKey(Order, null=True, on_delete = models.SET_NULL)
    quantity = models.IntegerField(default=0, null=True, blank=True, validators=[MinValueValidator(0)])
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        return self.product_size.product.price * self.quantity

class Rating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()

class Claim(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    description = models.TextField()
    date_submitted = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('product', 'order')

    def __str__(self):
        return f'Claim {self.id} by {self.customer.user.email}'
