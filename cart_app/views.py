from django.shortcuts import render, redirect
from product_app.models import Product
from .models import Cart
from accounts_app.forms import LoginForm, GuestForm
from billing_app.models import BillingProfile
from order_app.models import Order
from accounts_app.models import GuestModel
# Create your views here.

def cart_home(request):
    cart,new_obj = Cart.objects.new_or_get(request)
    return render(request,"cart/home.html",context={"cart": cart})

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
        cart_items = cart.products.count()
        request.session['cart_items'] = cart_items
        if cart_items==0:
            request.session['cart_items'] = ""
    return redirect("cart_app:cart_home")

def checkout_home(request):
    cart_obj,new_cart = Cart.objects.new_or_get(request)
    if new_cart or cart_obj.products.all() ==0:
        return redirect("cart_app:cart_home")
    order_obj, new_order = Order.objects.get_or_create(cart=cart_obj)
    
    user = request.user
    billing_profile = None
    login_form = LoginForm()
    guest_form = GuestForm()
    guest_email_id = request.session.get("guest_email_id")
    if user.is_authenticated and user.email:
        billing_profile, billing_profile_created = BillingProfile.objects.get_or_create(user=user,email=user.email)
    elif guest_email_id is not None:
        guest_email_obj = GuestModel.objects.get(id=guest_email_id)
        billing_profile, billing_profile_guest_created = BillingProfile.objects.get_or_create(email=guest_email_obj.email)

    context = {
        "object": order_obj,
        "billing_profile": billing_profile,
        "login_form": login_form,
        "guest_form": guest_form,
    }

    return render(request, "checkout/home.html",context)
