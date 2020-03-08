from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager
)

class UserManager(BaseUserManager):
    def create_user(self, name, email, password, is_active=True, is_staff=False, is_admin=False):
        if not email:
            raise ValueError("Users must enter email")
        if not password:
            raise ValueError("Users must enter password")
        if not name:
            raise ValueError("User must enter name")
        user_obj = self.model(
            email = self.normalize_email(email)
        )
        user_obj.set_password(password) #also way to change password
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.active = is_active
        user_obj.name = name
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, name, email, password=None):
        user = self.create_user(
            email=email,
            name=name,
            password=password,
            is_staff=True
        )
        return user

    def create_superuser(self, name, email, password=None):
        user = self.create_user(
            email=email,
            name=name,
            password=password,
            is_admin=True,
            is_staff=True
        )
        return user

# AbstractBaseUser is the django built-in user model, which we are going to extend
class User(AbstractBaseUser):
    email = models.EmailField(unique=True, max_length=50)
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    name = models.CharField(max_length=30,default="")

    objects = UserManager()

    # thus, we could login using email as django takes username to login
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email

    def has_perm(self, perm):
        return True
    
    def has_module_perms(self, app_label):
        return True
    
    # with property, we can get value like person.is_staff instead of calling func like person.is_staff()
    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin
        
    @property
    def is_active(self):
        return self.active

class GuestModel(models.Model):
    email = models.EmailField()
    active = models.BooleanField(default=True)
    upated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email