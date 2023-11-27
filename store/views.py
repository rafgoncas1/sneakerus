from django.shortcuts import get_object_or_404, render, redirect

from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import *
from .forms import LoginForm, PaymentDataForm, RegisterForm, CustomerForm, ShippingAddressForm
from django.contrib.auth import login, logout
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse
import json



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
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer, status=Status.objects.get(name='No realizado'))
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']
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
        'cartItems': cartItems,
    }
    return render(request, 'store/store.html', context)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer, status=Status.objects.get(name='No realizado'))
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/cart.html', context)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer, status=Status.objects.get(name='No realizado'))
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']
    
    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/checkout.html', context)

def about(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer, status=Status.objects.get(name='No realizado'))
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']
    
    context = {'cartItems': cartItems}
    return render(request, 'store/about.html', context)

def productDetails(request, producto_id):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer, status=Status.objects.get(name='No realizado'))
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']
        
    producto = get_object_or_404(Product, pk=producto_id)
    colors = producto.productcolor_set.all()

    # sizes ordered by name
    sizes = producto.productsize_set.all().order_by('size__name')
    return render(request, 'store/product.html', {'product': producto, 'colors': colors, 'sizes': sizes, 'cartItems': cartItems})


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


def profile(request, customer_id):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer, status=Status.objects.get(name='No realizado'))
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']
    customer = Customer.objects.get(user=request.user)
    customer_id = customer.id
    shipping_address = ShippingAddress.objects.filter(customer=customer)
    return render(request, 'store/profile.html', {'customer': customer, 'shipping_address': shipping_address, 'customer_id': customer_id, 'cartItems': cartItems})

def create_update_delivery(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer, status=Status.objects.get(name='No realizado'))
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']
    customer = request.user.customer
    shipping_address = customer.shippingaddress_set.last()
    form = ShippingAddressForm(request.POST or None, instance=shipping_address)
    if request.method == 'POST':
        if form.is_valid():
            new_shipping_address = form.save(commit=False)
            new_shipping_address.customer = customer
            new_shipping_address.save()
            return redirect('store')
    return render(request, 'store/delivery_form.html', {'form': form, 'customer': customer, 'cartItems': cartItems})

def create_update_payment(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer, status=Status.objects.get(name='No realizado'))
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']
    customer = request.user.customer
    payment_data = customer.paymentdata_set.last()
    form = PaymentDataForm(request.POST or None, instance=payment_data)
    if request.method == 'POST':
        if form.is_valid():
            new_payment_data = form.save(commit=False)
            new_payment_data.customer = customer
            new_payment_data.save()
            return redirect('store')
    return render(request, 'store/payment_form.html', {'form': form, 'customer': customer, 'cartItems': cartItems})

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

  
def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    size_name = data['size']
    action = data['action']
    
    customer = Customer.objects.get_or_create(user=request.user)[0]
    product_size = ProductSize.objects.get(size=Size.objects.get(name=size_name), product=Product.objects.get(id=productId))
    if not product_size:
            return JsonResponse({'error': 'No existe la talla del producto'}, safe=False)
    order, created = Order.objects.get_or_create(customer=customer, status=Status.objects.get(name='No realizado'))    
    orderItem, created = OrderItem.objects.get_or_create(order=order, product_size=product_size)
    if action == 'add':
        try:
            quantity = int(data['quantity'])
        except:
            return JsonResponse({'error': 'Cantidad inválida'}, safe=False)
        if product_size.stock - quantity < 0:
            return JsonResponse({'error': 'Talla no disponible para la cantidad seleccionada'}, safe=False)
        
        product_size.stock = product_size.stock - quantity
        product_size.save()

        orderItem.quantity = orderItem.quantity + quantity
        orderItem.save()
        return JsonResponse({"success": "Se ha añadido el producto a la cesta"}, safe=False)
    elif action == 'remove':
        orderItem.quantity = orderItem.quantity - 1
        orderItem.save()
        product_size.stock = product_size.stock + 1
        product_size.save()
    
    
    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse({}, safe=False)

def track_orders(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer, status=Status.objects.get(name='No realizado'))
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']
    if request.method == 'POST':
        tracking_id = request.POST.get('tracking_id')
        if tracking_id:
            tracking = Order.objects.exclude(status=Status.objects.get(name='No realizado')).filter(tracking_id=tracking_id)
            if tracking:
                return HttpResponseRedirect("/tracking/" + tracking_id)
            else:
                return render(request, 'store/track_order.html', {'cartItems': cartItems})
        else:
            return render(request, 'store/track_order.html', {'error_message': 'Por favor, proporciona un ID de seguimiento.', 'cartItems': cartItems})
    return render(request, 'store/track_order.html', {'cartItems': cartItems})

def track_order(request, tracking_id):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer, status=Status.objects.get(name='No realizado'))
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']
    try:
        order = get_object_or_404(Order, tracking_id=tracking_id)
        order_items = OrderItem.objects.filter(order=order)

        # Calcular el costo total del pedido
        total_cost = order.get_cart_total

        context = {'order': order, 'order_items': order_items, 'total_cost': total_cost, 'cartItems': cartItems}
    except Order.DoesNotExist:
        return render(request, 'store/track_order.html', {'error_message': f'No existe un pedido con ID de seguimiento {tracking_id}.'})

    return render(request, 'store/track_order_status.html', context)

@login_required
def view_orders(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer, status=Status.objects.get(name='No realizado'))
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']
    # orders with status distinct from 'No realizado'
    user_orders = Order.objects.exclude(status=Status.objects.get(name='No realizado')).order_by('-date_ordered')
    context = {'user_orders': user_orders, 'cartItems': cartItems}
    return render(request, 'store/view_orders.html', context)

