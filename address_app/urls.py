from django.urls import path
from .views import checkout_create_address

urlpatterns = [
    path('checkout-address', checkout_create_address, name='checkout_create_address'),
]