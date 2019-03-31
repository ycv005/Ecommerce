from django.shortcuts import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .models import ContactForm, LoginForm, RegisterForm

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

def login_page(request):
    form = LoginForm(request.POST or None)
    context = {
        "form":form
    }
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            # A backend authenticated the credentials
            login(request, user)
            return redirect("/")
        else:
            # No backend authenticated the credentials
            print("No such user")
        form = LoginForm()
    return render(request,"auth/login_page.html",context)

def register_page(request):
    form = RegisterForm(request.POST or None)
    context = {
        "form":form
    }

    if form.is_valid():
        username = form.cleaned_data.get("username")
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        new_user = User.objects.create_user(username,email,password)
        print(new_user)
        return redirect("/")
    return render(request,"auth/register_page.html",context)