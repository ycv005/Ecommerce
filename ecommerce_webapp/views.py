from django.shortcuts import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .models import ContactForm

def home_page(request):
    return render(request,"ecommerce_webapp/home_page.html",context={"title":"This is from the context"})

def contact_page(request):
    contact_form = ContactForm(request.POST or None)
    # if request.method=="POST":
    #     print(request.POST)
    #     print(request.POST.get("fullname"))
    if contact_form.is_valid():
        print(contact_form.cleaned_data)
    return render(request,"ecommerce_webapp/contact_page.html",{"form":contact_form})

def about_page(request):
    return render(request,"ecommerce_webapp/about_page.html",{})