from django.db import models
from django.conf import settings
from product_app.models import Product

User = settings.AUTH_USER_MODEL
class CartModelManager(models.Manager):
    def new_or_get(self, request):
        cart_id = request.session.get("cart_id",None)
        qs = self.get_queryset().filter(id=cart_id) 
        if qs.count()==1:
            new_obj = False
            cart_obj = qs.first()
            if request.user.is_authenticated and cart_obj.user is None:
                cart_obj.user = request.user
                cart_obj.save()
        else:
            new_obj = True
            cart_obj = Cart.objects.new_cart(user=request.user)
            request.session["cart_id"] = cart_obj.id
        return cart_obj,new_obj

    def new_cart(self, user=None):
        user_obj = None
        if user is not None and user.is_authenticated:
            user_obj = user
        return self.model.objects.create(user=user_obj)

# Create your models here.
class Cart(models.Model):
    user =models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE) #any user could create cart, ins
    total = models.DecimalField(default=0.00,max_digits=10, decimal_places=2)
    products = models.ManyToManyField(Product, blank=True)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = CartModelManager()

    def  __str__(self):
        return str(self.id)
