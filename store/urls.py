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
    path('user/<int:user_id>/', views.profile, name='profile'),
    path('user/<int:user_id>/update/delivery/', views.updateDelivery, name='update_delivery'),
    path('user/<int:user_id>/update/payment/', views.updatePayment, name='update_payment'),
    path('customerlist/', views.customer_list, name='customer_list'),
    path('customercreate/', views.customer_create, name='customer_create'),
    path('customerupdate/<int:customer_id>/', views.customer_update, name='customer_update'),
    path('customerdelete/<int:customer_id>/', views.customer_delete, name='customer_delete')
    ]