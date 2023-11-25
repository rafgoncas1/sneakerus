from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from .models import *
from .forms import LoginForm, RegisterForm
from django.contrib.auth import login, logout
from django.shortcuts import redirect
from django.contrib.auth import authenticate
from django.http import JsonResponse
import json
from django.contrib.auth.decorators import login_required

def store(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer, status=Status.objects.get(name='No realizado'))
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']

    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}
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
        if product_size.stock <= 0:
            return JsonResponse({'error': 'Talla no disponible'}, safe=False)
        
        product_size.stock = product_size.stock - 1
        product_size.save()

        orderItem.quantity = orderItem.quantity + 1
        orderItem.save()
    
    elif action == 'remove':
        orderItem.quantity = orderItem.quantity - 1
        orderItem.save()
        product_size.stock = product_size.stock + 1
        product_size.save()
    
    
    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse({"success": "Order updated successfully"}, safe=False)

def track_orders(request):
    if request.method == 'POST':
        tracking_id = request.POST.get('tracking_id')
        if tracking_id:
            return HttpResponseRedirect(reverse('tracking', args=[tracking_id]))
        else:
            return render(request, 'store/track_order.html', {'error_message': 'Por favor, proporciona un ID de seguimiento.'})
    return render(request, 'store/track_order.html')

def track_order(request, tracking_id):
    try:
        order = get_object_or_404(Order, tracking_id=tracking_id)
        order_items = OrderItem.objects.filter(order=order)

        # Calcular el costo total del pedido
        total_cost = order.calculate_total_price()
        print(total_cost)

        context = {'order': order, 'order_items': order_items, 'total_cost': total_cost}
    except Order.DoesNotExist:
        return render(request, 'store/track_order.html', {'error_message': f'No existe un pedido con ID de seguimiento {tracking_id}.'})

    return render(request, 'store/track_order_status.html', context)

@login_required
def view_orders(request):
    user_orders = Order.objects.filter(customer=request.user.customer)
    context = {'user_orders': user_orders}
    return render(request, 'store/view_orders.html', context)
