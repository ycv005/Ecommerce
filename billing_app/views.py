from django.shortcuts import render, reverse, HttpResponse, redirect
from django.views.generic import DetailView
from django.http import JsonResponse
from django.utils.http import is_safe_url
from .models import BillingProfile
# Create your views here.
import stripe

stripe.api_key = "sk_test_0nAn8OgmI7bM0E2uJr4oXRGU00NAoPjis6"
STRIPE_PUB_KEY = "pk_test_yAygi652saqFMbGVd2CF4kei00gBeICVmz"

def payment_method_view(request):
    # if request.user.is_authenticated:
    #     # since, a user have billing profile
    #     billing_profile = request.user.billingprofile
    #     customer_id = billing_profile.customer_id
    
    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    if not billing_profile:
        return redirect("/login")
    # next_url = None
    # next_ = request.GET.get('next')
    # if is_safe_url(next,request.get_host()):
    #     next_url = next_
    return render(request, 'billing_app/payment-method.html', {"publish_key": STRIPE_PUB_KEY,
    #   "next_url": next_url
      })

def payment_method_createview(request):
    if request.method == "POST" and request.is_ajax():
        billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
        if not billing_profile:
            return HttpResponse("Cannot find this user",status_code=401)
        # https://stripe.com/docs/api/cards/create?lang=python
        token = request.POST.get("token")
        if token is not None:
            customer = stripe.Customer.retrieve(billing_profile.customer_id)
            card = stripe.Customer.create_source(
            customer.id,
                source=token,
                )
        return JsonResponse({"msg": "here is the msg"})
    return HttpResponse("Error",status_code=401)