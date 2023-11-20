from django.shortcuts import get_object_or_404, render
from .models import *
from .forms import LoginForm, RegisterForm
from django.contrib.auth import login, logout
from django.shortcuts import redirect
from django.contrib.auth import authenticate

def store(request):
    products = Product.objects.all()
    context = {'products': products}
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
    
def search(request):
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

    return render(request, 'store/search.html', context)
