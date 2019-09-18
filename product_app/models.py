from django.db import models
import os
from .utils import get_unique_slug
from django.db.models.signals import pre_save

def user_directory_path(instance,filename):
    base_name = os.path.basename(filename)
    name,ext = os.path.splitext(base_name)

    return "product_app/IMG_" + str(instance.pk)+ext #it will be appended to the media_root defined in the settings

# Modifying the model manager by overwriting on it.
class ProductManager(models.Manager):  
    def get_featured(self):
        qs = self.get_queryset().filter(featured=True)
        if qs.count()>0:
            return qs
        else:
            return None

    def get_by_id(self,id):
        qs = self.get_queryset().filter(id=id)
        if qs.count()==1:
            return qs.first()
        else:
            return None

# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length = 100)
    description = models.TextField()
    price = models.DecimalField(max_digits=20, decimal_places=2,default=0)
    # image = models.ImageField(upload_to="product_app",null=True) #file added to- media_root/product_app
    image = models.ImageField(upload_to=user_directory_path,null=True,blank=True) #blank is validation check(for django), null is for database 
    featured = models.BooleanField(default=False)
    objects = ProductManager() #extend the Objects Manager of the Product
    slug = models.SlugField(blank=True, unique=True)

    def get_absolute_url(self):
        return "/product/{slug}/".format(slug=self.slug)

    def __str__(self):
        return self.title

def product_pre_save_receiver(sender, instance, *args,**kwargs):
    if not instance.slug:
        instance.slug = get_unique_slug(instance)

pre_save.connect(product_pre_save_receiver,sender=Product)
# befor the Product model get saved into db, pre_save is perform