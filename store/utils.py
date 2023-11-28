import json
from . models import *


def cookieCart(request):

    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
    items = []
    order = {'get_cart_total': 0, 'get_cart_items': 0}
    cartItems = order['get_cart_items']

    for i in cart:
        try:
            cartItems += int(cart[i]['quantity'])
            product = Product.objects.get(id=cart[i]['productId'])
            total = (product.price * int(cart[i]['quantity']))
            order['get_cart_total'] += total
            order['get_cart_items'] += int(cart[i]['quantity'])

            item  = {}
            item['product_size'] = {}
            item['product_size']['product'] = product
            item['product_size']['size'] = Size.objects.get(name=cart[i]['size'])
            item['quantity'] = int(cart[i]['quantity'])
            item['get_total'] = item['quantity'] * product.price
            items.append(item)
        except:
            pass
    return {'cartItems': cartItems, 'order': order, 'items': items}

def cartData(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer, status=Status.objects.get(name='No realizado'))
        cartItems = order.get_cart_items
        items = order.orderitem_set.all()
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']

    return {'cartItems': cartItems, 'order': order, 'items': items}