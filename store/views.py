from django.shortcuts import get_object_or_404, render, redirect
from .models import *
from .forms import LoginForm, RegisterForm, CustomerForm
from django.contrib.auth import login, logout
from django.shortcuts import redirect
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages




def store(request):
    query = request.GET.get('q', '')

    colors = Color.objects.all()
    sizes = Size.objects.all()
    brands = Brand.objects.all()

    color_id = request.GET.get('color', '')
    size_id = request.GET.get('talla', '')
    brand_id = request.GET.get('marca', '')

    filters = {}
    filters_applied = ""
    if color_id:
        color = colors.get(id=color_id)
        filters['productcolor__color__id'] = color_id
        filters_applied += f"Color: {color.name}. "
    if size_id:
        size = sizes.get(id=size_id)
        filters['productsize__size__id'] = size_id
        filters_applied += f"Talla: {size.name}. "
    if brand_id:
        brand = brands.get(id=brand_id)
        filters['brand__id'] = brand_id
        filters_applied += f"Marca: {brand.name}. "

    products = Product.objects.filter(name__icontains=query, **filters)

    context = {
        'products': products, 
        'query': query, 
        'colors': colors, 
        'sizes': sizes, 
        'brands': brands, 
        'color_id': color_id, 
        'size_id': size_id, 
        'brand_id': brand_id,
        'filters_applied': filters_applied,
    }
    return render(request, 'store/store.html', context)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer, status=Status.objects.get(name='No realizado'))
        items = order.orderitem_set.all()
    else:
        items = []

    context = {'items': items}
    return render(request, 'store/cart.html', context)

def checkout(request):
    context = {}
    return render(request, 'store/checkout.html')

def about(request):
    context = {}
    return render(request, 'store/about.html')

def productDetails(request, producto_id):
    # Obtén el objeto Producto con el ID proporcionado
    producto = get_object_or_404(Product, pk=producto_id)
    colors = producto.productcolor_set.all()
    sizes = producto.productsize_set.all()
    return render(request, 'store/detail_product.html', {'product': producto, 'colors': colors, 'sizes': sizes})

def auth_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('store')
            else:
                form.add_error(None, 'Usuario o contraseña incorrectos')
                context = {'form': form}
                return render(request, 'store/login.html', context)
        else:
            form.add_error(None, form.errors)
            context = {'form': form}
            return render(request, 'store/login.html', context)
    else:
        form = LoginForm()
        context = {'form': form}
        return render(request, 'store/login.html', context)

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # create customer for user
            Customer.objects.create(user=user, email=user.email, name=form.cleaned_data['name'])
            login(request, user)
            return redirect('store')
        else:
            form.add_error(None, form.errors)
            context = {'form': form}
            return render(request, 'store/register.html', context)
    else:
        form = RegisterForm()
        context = {'form': form}
        return render(request, 'store/register.html', context)
    
def auth_logout(request):
    logout(request)
    return redirect('store')

def profile(request, user_id):
    customer = get_object_or_404(Customer, pk=user_id)
    shipping_address = ShippingAddress.objects.filter(customer=customer)
    return render(request, 'store/profile.html', {'customer': customer, 'shipping_address': shipping_address})

def updateDelivery(request, user_id):
    customer = get_object_or_404(Customer, pk=user_id)
    return render(request, 'store/update_delivery.html', {'customer': customer})

def updatePayment(request, user_id):
    customer = get_object_or_404(Customer, pk=user_id)
    return render(request, 'store/update_payment.html', {'customer': customer})

def user_has_perm(user):
    if not user.is_staff:
        return False
    return True

@login_required
@user_passes_test(user_has_perm, redirect_field_name=None)
def customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'store/customer_list.html', {'customers': customers})

@login_required
@user_passes_test(user_has_perm, redirect_field_name=None)
def customer_create(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('customer_list')
    else:
        form = CustomerForm()
    return render(request, 'store/customer_form.html', {'form': form})

@login_required
@user_passes_test(user_has_perm, redirect_field_name=None)
def customer_update(request, customer_id):
    customer = get_object_or_404(Customer, pk=customer_id)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('customer_list')
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'store/customer_form.html', {'form': form})

@login_required
@user_passes_test(user_has_perm, redirect_field_name=None)
def customer_delete(request, customer_id):
    customer = get_object_or_404(Customer, pk=customer_id)
    customer.delete()
    return redirect('customer_list')