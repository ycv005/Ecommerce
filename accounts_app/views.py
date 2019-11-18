from django.shortcuts import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .forms import LoginForm, RegisterForm
from django.utils.http import is_safe_url

# Create your views here.
def login_page(request):
    form = LoginForm(request.POST or None)
    context = {
        "form":form
    }
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        next_ = request.GET.get('next_url')
        next_post = request.POST.get('next_url')
        redirect_path = next_ or next_post or None
        if user is not None:
            # A backend authenticated the credentials
            login(request, user)
            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)
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