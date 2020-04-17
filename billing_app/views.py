from django.shortcuts import render, reverse, HttpResponse, redirect
from django.views.generic import DetailView
from django.http import JsonResponse
from django.utils.http import is_safe_url
from .models import BillingProfile, Card
from django.conf import settings
import stripe
from django.urls import reverse

STRIPE_SECRET_KEY = getattr(settings,"STRIPE_SECRET_KEY")
stripe.api_key = STRIPE_SECRET_KEY
STRIPE_PUB_KEY = getattr(settings,"STRIPE_PUB_KEY")


def payment_method_view(request):
    # if request.user.is_authenticated:
    #     # since, a user have billing profile
    #     billing_profile = request.user.billingprofile
    #     customer_id = billing_profile.customer_id
    
    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    if not billing_profile:
        return redirect("/login")
    next_url = None
    next_ = request.GET.get('next')
    if is_safe_url(next_,request.get_host()):
        next_url = next_
    if not next_url:
        next_url = reverse('cart_app:on_success')
    return render(request, 'billing_app/payment-method.html', {"publish_key": STRIPE_PUB_KEY,
      "next_url": next_url
      })

def payment_method_createview(request):
    if request.method == "POST" and request.is_ajax():
        billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
        if not billing_profile:
            return HttpResponse("Cannot find this user",status_code=401)
        # https://stripe.com/docs/api/cards/create?lang=python
        token = request.POST.get("token")
        if token is not None:
            new_card_obj = Card.objects.add_new(billing_profile,token)
            
        return JsonResponse({"msg": "here is the msg"})
    return HttpResponse("Error",status=401)