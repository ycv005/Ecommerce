from django.db import models
from django.conf import settings
from product_app.models import Product

User = settings.AUTH_USER_MODEL

# Create your models here.
class Cart(models.Model):
    user =models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE) #any user could create cart, ins
    total = models.DecimalField(default=0.00,max_digits=10, decimal_places=2)
    products = models.ManyToManyField(Product, blank=True)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def  __str__(self):
        return str(self.id)
