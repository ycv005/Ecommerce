from django.shortcuts import render
from .models import Cart
# Create your views here.

def cart_create():
    cart = Cart.object.create(user=None)
    return cart

def cartHome(request):
    # following is the way to check all the variables present in the req session
    # for key, value in request.session.items():
    #     print('{} => {}'.format(key, value))
    cart_id = request.session.get("cart_id",None)
    qs = Cart.object.filter(id=cart_id) 
    if qs.count()==1: #if cart_id exist in database then good
        cart = qs.first()
    else:   #cart_id doesn't matches
        cart =cart_create()
        request.session["cart_id"] = cart.id

    return render(request,"cart/home.html",context={})