from django.shortcuts import render, reverse, HttpResponse
from django.views.generic import DetailView
from django.http import JsonResponse
from django.utils.http import is_safe_url
# Create your views here.

STRIPE_PUB_KEY = "pk_test_yAygi652saqFMbGVd2CF4kei00gBeICVmz"

def payment_method_view(request):
    # next_url = None
    # next_ = request.GET.get('next')
    # if is_safe_url(next,request.get_host()):
    #     next_url = next_
    return render(request, 'billing_app/payment-method.html', {"publish_key": STRIPE_PUB_KEY,
    #   "next_url": next_url
      })

def payment_method_createview(request):
    if request.method == "POST" and request.is_ajax():
        return JsonResponse({"msg": "here is the msg"})
    return HttpResponse("Error",status_code=401)