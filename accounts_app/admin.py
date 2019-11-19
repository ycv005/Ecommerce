from django.contrib import admin

# Register your models here.
from .models import GuestModel

admin.site.register(GuestModel)