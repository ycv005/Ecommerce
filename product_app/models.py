from django.db import models
import os


def user_directory_path(instance,filename):
    base_name = os.path.basename(filename)
    name,ext = pytos.path.splitext(base_name)
    return "product_app/IMG_" + str(instance.pk)+ext

# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length = 100)
    description = models.TextField()
    price = models.DecimalField(max_digits=20, decimal_places=2,default=0)
    # image = models.ImageField(upload_to="product_app",null=True) #file added to- media_root/product_app
    image = models.ImageField(upload_to=user_directory_path,null=True) 

    def __str__(self):
        return self.title