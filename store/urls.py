from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name='store'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('about/', views.about, name='about'),
    path('producto/<int:producto_id>/', views.productDetails, name='detalle_producto'),
    path('login/', views.auth_login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.auth_logout, name='logout'),
    path('seguimiento/', views.track_orders, name='track_orders'),
    path('track_order/<str:tracking_id>/', views.track_order, name='track_order'),
    path('orders/', views.view_orders, name='view_orders'),


]