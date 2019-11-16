from django.db import models
from cart_app.models import Cart
# Create your models here.

# db value on left, human readable on right
ORDER_STATUS_CHOICES  = (
    ("created","Created"),
    ("paid","Paid"),
    ("shipped","Shipped"),
    ("refunded","Refunded"),
)

class Order(models.Model):
    order_id = models.CharField(max_length=120, blank=True)
    cart= models.ForeignKey(Cart, on_delete=models.CASCADE)
    shipping_total = models.DecimalField(default =0.0, max_digits=10, decimal_places=2) 
    total = models.DecimalField(default =0.0, max_digits=10, decimal_places=2)
    status = models.CharField(default = "created", choices=ORDER_STATUS_CHOICES, max_length=120)
    # shipping address = 
    # billing address =
    # billing profile = 

    def __str__(self):
        return self.order_id
