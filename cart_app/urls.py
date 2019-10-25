from django.urls import path
from .views import cartHome

urlpatterns = [
    path('', cartHome,name='cart'),
]