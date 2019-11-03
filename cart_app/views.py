from django.shortcuts import render
from .models import Cart
# Create your views here.

def cartHome(request):
    cart,new_obj = Cart.objects.new_or_get(request)
    return render(request,"cart/home.html",context={})