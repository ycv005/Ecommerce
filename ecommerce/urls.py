"""ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from cart_app.views import cart_detail_api_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("ecommerce_webapp.urls")),
    path("product/", include(("product_app.urls", 'product_app'), namespace="product_app")),
    path("search/", include(("search_app.urls", 'search_app'), namespace="search_app")),
    path("cart/", include(("cart_app.urls", 'cart_app'), namespace="cart_app")),
    path("address/", include(("address_app.urls", 'address_app'), namespace="address_app")),
    path("api/cart/", cart_detail_api_view,name='cart_detail_api_view'),
]
