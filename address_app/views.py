from django.shortcuts import render,redirect

from django.utils.http import is_safe_url
from billing_app.models import BillingProfile

from address_app.forms import AddressForm
# Create your views here.

def checkout_create_address(request):
    form = AddressForm(request.POST or None)
    context = {
        "form":form
    }
    print("handling checkout create address")
    if form.is_valid():
        instance = form.save(commit=False)
        billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
        if billing_profile is not None:
            instance.billing_profile = billing_profile
            instance.save()
            request.session['address_id'] = instance.id

        next_ = request.GET.get('next_url')
        next_post = request.POST.get('next_url')
        redirect_path = next_ or next_post or None
        if is_safe_url(redirect_path, request.get_host()):
            print("redirect path is-",redirect_path)
            return redirect(redirect_path)
    return redirect("cart_app:checkout")