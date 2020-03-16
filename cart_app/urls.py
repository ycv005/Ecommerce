from django.urls import path
from .views import cart_home, cart_udpate, checkout_home, on_success, cart_detail_api_view
from billing_app.views import payment_method_view, payment_method_createview

urlpatterns = [
    path('', cart_home,name='cart_home'),
    path('update', cart_udpate,name='cart_update'),
    path('checkout', checkout_home,name='checkout'),
    path('success', on_success,name='on_success'),
    path('billing',payment_method_view,name='billing_payment'),
    path('billing-create',payment_method_createview,name='billing_payment_create'),
]