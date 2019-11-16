from django.urls import path
from .views import cart_home, cart_udpate, checkout_home

urlpatterns = [
    path('', cart_home,name='cart_home'),
    path('update', cart_udpate,name='cart_update'),
    path('checkout', checkout_home,name='checkout'),
]