from django.db import models

# Create your models here.

class GuestModel(models.Model):
    email = models.EmailField()
    active = models.BooleanField(default=True)
    upated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email