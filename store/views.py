from django.shortcuts import get_object_or_404, render
from .models import *

def store(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'store/store.html', context)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer, status='No Realizado')
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
       

    # Puedes agregar lógica adicional aquí si es necesario

    # Renderiza la plantilla de detalle_producto.html con el producto
    return render(request, 'store/detail_product.html', {'product': producto})