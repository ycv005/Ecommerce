from django.db import models
import os
from django.db.models import Q
from .utils import get_unique_slug
from django.db.models.signals import pre_save
from django.urls import reverse

def user_directory_path(instance,filename):
    base_name = os.path.basename(filename)
    name,ext = os.path.splitext(base_name)

    return "product_app/IMG_" + str(instance.pk)+ext #it will be appended to the media_root defined in the settings

# Modified QuerySet
class ProductQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)

    def search(self, query):
        lookup = Q(title__icontains=query) | Q(description__icontains=query) #lookup in the title and description
        return self.filter(lookup).distinct()

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

    def search(self,query):
        return self.get_queryset().active().search(query)

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
    timestamp = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        # return "/product/{slug}/".format(slug=self.slug) #this one is hardcoded one
        return reverse("product_app:urldetail", kwargs={"slug":self.slug}) #urldetail is the name of the defined in the product/url.py, so url is change from there, it will be change here too.
        # example of the nested slug
    def __str__(self):
        return self.title

def product_pre_save_receiver(sender, instance, *args,**kwargs):
    if not instance.slug:
        instance.slug = get_unique_slug(instance)

pre_save.connect(product_pre_save_receiver,sender=Product)
# befor the Product model get saved into db, pre_save is perform