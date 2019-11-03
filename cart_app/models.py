from django.db import models
from django.conf import settings
from product_app.models import Product
from django.db.models.signals import m2m_changed, pre_save

User = settings.AUTH_USER_MODEL
class CartModelManager(models.Manager):
    # to handle case, 1 user is having more tha
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
    subtotal = models.DecimalField(default=0.00,max_digits=10, decimal_places=2)
    products = models.ManyToManyField(Product, blank=True)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = CartModelManager()

    def  __str__(self):
        return str(self.id)

def m2m_changed_cart_total_receiver(sender, instance, action, **kwargs):
    if action=="post_remove" or action =="post_add" or action =="post_clear":
        subtotal =0
        products = instance.products.all()
        for i in products:
            subtotal+=i.price
        instance.subtotal = subtotal
        instance.save()
        # you could also total here as well, just to expand more it done so

m2m_changed.connect(m2m_changed_cart_total_receiver, sender=Cart.products.through)

def pre_save_cart_receiver(sender, instance, *args, **kwargs):
    instance.total  = instance.subtotal
    # instance.save() here will cause max dep. recursion error.

pre_save.connect(pre_save_cart_receiver, sender=Cart)