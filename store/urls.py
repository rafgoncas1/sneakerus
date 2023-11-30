from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name='store'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('about/', views.about, name='about'),
    path('product/<int:producto_id>/', views.productDetails, name='details'),
    path('login/', views.auth_login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.auth_logout, name='logout'),
    path('customer/<int:customer_id>/', views.profile, name='profile'),
    path('customer/update/delivery/', views.create_update_delivery, name='create_update_delivery'),
    path('customer/update/payment/', views.create_update_payment, name='create_update_payment'),
    path('customerlist/', views.customer_list, name='customer_list'),
    path('customercreate/', views.customer_create, name='customer_create'),
    path('customerupdate/<int:customer_id>/', views.customer_update, name='customer_update'),
    path('customerdelete/<int:customer_id>/', views.customer_delete, name='customer_delete'),
    path('update_item/', views.updateItem, name='update_item'),
    path('process_order/', views.processOrder, name='process_order'),
    path('tracking/', views.track_orders, name='track_orders'),
    path('tracking/<str:tracking_id>/', views.track_order, name='track_order'),
    path('orders/', views.view_orders, name='view_orders'),
]

