from django.shortcuts import render, redirect
from product_app.models import Product
from .models import Cart
# Create your views here.

def cart_home(request):
    cart,new_obj = Cart.objects.new_or_get(request)
    return render(request,"cart/home.html",context={})

def cart_udpate(request):
    product_id = request.POST.get("product_id")
    if product_id is not None:
        try:
            prod_obj = Product.objects.get_by_id(id=product_id)
        except Product.DoesNotExist:
            return redirect("cart_app:cart_home")
        cart,new_obj = Cart.objects.new_or_get(request)
        if prod_obj in cart.products.all():
            cart.products.remove(prod_obj)
        else:
            cart.products.add(prod_obj) # cart.products.add(product_id)
        # above is the way to update many-to-many field, while cart.title = "hello" it is update like this
        # adding cart's many to many field is changing, we need to call save, but we already define signal m2m_change in the cart model.
    return redirect("cart_app:cart_home")