from django.urls import path
from .views import cart_home, cart_udpate

urlpatterns = [
    path('', cart_home,name='cart_home'),
    path('update', cart_udpate,name='cart_update'),
]