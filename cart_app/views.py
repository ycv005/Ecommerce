from django.shortcuts import render

# Create your views here.

def cartHome(request):

    return render(request,"cart/home.html",context={})