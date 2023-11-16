from django.shortcuts import render

def store(request):
    context = {}
    return render(request, 'store/store.html', context)

def cart(request):
    context = {}
    return render(request, 'store/cart.html')

def checkout(request):
    context = {}
    return render(request, 'store/checkout.html')

def about(request):
    context = {}
    return render(request, 'store/about.html')