from django.shortcuts import render

# Create your views here.

def cartHome(request):
    # following is the way to check all the variables present in the req session
    # for key, value in request.session.items():
    #     print('{} => {}'.format(key, value))
    cart_id = request.session.get("cart_id",None) #
    if cart_id is None:
        request.session["cart_id"] = 121
    return render(request,"cart/home.html",context={})