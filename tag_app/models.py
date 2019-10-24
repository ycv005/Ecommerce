from django.db import models
from product_app.utils import get_unique_slug
from product_app.models import Product
from django.db.models.signals import pre_save

# Create your models here.
class ProductTag(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField()
    timestamp = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    product = models.ManyToManyField(Product, blank=True)

    def __str__(self):
        return self.title
        
def tag_pre_save_receiver(sender, instance, *args,**kwargs):
    if not instance.slug:
        instance.slug = get_unique_slug(instance)

pre_save.connect(tag_pre_save_receiver,sender=ProductTag)
