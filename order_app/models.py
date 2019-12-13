import math
from django.db import models
from billing_app.models import BillingProfile
from cart_app.models import Cart
from address_app.models import AddressModel
# when importing model from X to Y then in X, you can't import Y. this will create infinity loop.

# Create your models here.
from django.db.models.signals import pre_save, post_save
from ecommerce.utils import unique_order_id_generator

# db value on left, human readable on right
ORDER_STATUS_CHOICES  = (
    ("created","Created"),
    ("paid","Paid"),
    ("shipped","Shipped"),
    ("refunded","Refunded"),
)

class OrderManager(models.Manager):
    def new_or_get(self, billing_profile, cart_obj):
        created= False
        # qs = Order.objects.filter(billing_profile=billing_profile, cart=cart_obj, active=True)
        qs = self.get_queryset().filter(billing_profile=billing_profile, cart=cart_obj, active=True)
        if qs.count()==1:
            obj = qs.first()
        else:
            # obj = Order.objects.create(billing_profile=billing_profile, cart=cart_obj)
            obj = self.model.objects.create(billing_profile=billing_profile, cart=cart_obj)
            created = True
        return obj, created

class Order(models.Model):
    order_id = models.CharField(max_length=120, blank=True)
    cart= models.ForeignKey(Cart, on_delete=models.CASCADE)
    shipping_total = models.DecimalField(default =50.00, max_digits=10, decimal_places=2) 
    total = models.DecimalField(default =0.0, max_digits=10, decimal_places=2)
    status = models.CharField(default = "created", choices=ORDER_STATUS_CHOICES, max_length=120)
    billing_profile = models.ForeignKey(BillingProfile, on_delete=models.CASCADE, null=True, blank=True)
    active = models.BooleanField(default=True)
    address = models.ForeignKey(AddressModel, on_delete=models.CASCADE, null=True, blank=True)

    def update_total(self):
        total = math.fsum([self.cart.total,self.shipping_total])
        self.total = format(total, '.2f') 
        self.save()

    objects = OrderManager()
    def __str__(self):
        return self.order_id

def pre_save_create_order_id(sender, instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id = unique_order_id_generator(instance)
# there is no need to call instance.save() in pre_save
    older_order_qs = Order.objects.exclude(billing_profile=instance.billing_profile).filter(cart=instance.cart, active=True)
    if older_order_qs.exists():
        older_order_qs.update(active=False)

def post_save_cart_total(sender, instance, created, *args, **kwargs):
    # instance will of Cart, as mention in sender of post save
    if not created:
        cart_id = instance.id
        qs = Order.objects.filter(cart__id=cart_id)
        if qs.count()==1:
            order_obj = qs.first()
            order_obj.update_total()

def post_save_order(sender, instance, created, *args, **kwargs):
    if created:
        instance.update_total()

pre_save.connect(pre_save_create_order_id, sender=Order)

post_save.connect(post_save_order, sender=Order)

# read statement on top, why we are working here for Cart
post_save.connect(post_save_cart_total, sender=Cart)