from django.shortcuts import render, redirect
from product_app.models import Product
from django.http import JsonResponse
from .models import Cart
from accounts_app.forms import LoginForm, GuestForm
from billing_app.models import BillingProfile
from address_app.forms import AddressForm
from address_app.models import AddressModel
from order_app.models import Order
from accounts_app.models import GuestModel
from django.http import JsonResponse
from django.conf import settings
import stripe

STRIPE_PUB_KEY = getattr(settings,"STRIPE_PUB_KEY")

def cart_detail_api_view(request):
    cart,new_obj = Cart.objects.new_or_get(request)
    products = [{
        "id": p.id,
        "url": p.get_absolute_url(),
        "name": p.title, 
        "price": p.price} 
        for p in cart.products.all()]
    return JsonResponse({"products": products, "subtotal": cart.subtotal, "total": cart.total})

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
            product_added = False
        else:
            product_added = True
            cart.products.add(prod_obj) # cart.products.add(product_id)
        # above is the way to update many-to-many field, while cart.title = "hello" it is update like this
        # adding cart's many to many field is changing, we need to call save, but we already define signal m2m_change in the cart model.
        cart_items = cart.products.count()
        request.session['cart_items'] = cart_items
        if cart_items==0:
            request.session['cart_items'] = ""
        if request.is_ajax():
            json_data = {
                "product_added": product_added,
                "cartItemCount": cart_items,
            }
            return JsonResponse(json_data)
    return redirect("cart_app:cart_home")

def checkout_home(request):
    cart_obj,new_cart = Cart.objects.new_or_get(request)
    if new_cart or cart_obj.products.all() ==0:
        return redirect("cart_app:cart_home")

    # user = request.user
    login_form = LoginForm()
    guest_form = GuestForm()
    address_form = AddressForm()
    address_id = request.session.get("address_id")
    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    # Not to make order for the cart until, we have a billing profile
    order_obj = None
    address_qs = None
    has_card = False
    if billing_profile is not None:
        address_qs=  AddressModel.objects.filter(billing_profile=billing_profile)
        order_obj, order_created  = Order.objects.new_or_get(billing_profile=billing_profile, cart_obj=cart_obj)
        if address_id:
            order_obj.address = AddressModel.objects.get(id=address_id)
            del request.session["address_id"]
            order_obj.save()
        has_card = billing_profile.has_card

    if request.method == "POST":
        order_obj_status = order_obj.is_done()
        print("order_obj_status",order_obj_status)
        if order_obj_status:
            did_charge, seller_msg = billing_profile.charge(order_obj)
            print("did_charge",did_charge)
            if did_charge:
                order_obj.mark_paid()
                request.session['cart_items']=0
                del request.session['cart_id']
                return redirect("cart_app:on_success")
            else:
                print(seller_msg)
                return redirect("cart_app:billing_payment")
            
    context = {
        "object": order_obj,
        "billing_profile": billing_profile,
        "login_form": login_form,
        "guest_form": guest_form,
        "address_form": address_form,
        "address_qs": address_qs,
        "has_card": has_card,
        "publish_key": STRIPE_PUB_KEY,
    }

    return render(request, "checkout/home.html",context)

def on_success(request):
    return render(request,"checkout/success.html")