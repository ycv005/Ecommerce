from django.db import models
# Create your models here.
from django.conf import settings
from django.db.models.signals import post_save, pre_save
from accounts_app.models import GuestModel

User = settings.AUTH_USER_MODEL
import stripe
stripe.api_key = "sk_test_0nAn8OgmI7bM0E2uJr4oXRGU00NAoPjis6"

class BillingProfileManager(models.Manager):
    def new_or_get(self, request):
        user = request.user
        created = False
        guest_email_id = request.session.get("guest_email_id")
        if user.is_authenticated and user.email:
            obj, created = self.model.objects.get_or_create(user=user,email=user.email)
        elif guest_email_id is not None:
            guest_email_obj = GuestModel.objects.get(id=guest_email_id)
            obj, created = self.model.objects.get_or_create(email=guest_email_obj.email)
        else:
            obj = None
        return obj, created

class BillingProfile(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    email = models.EmailField()
    active = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    customer_id = models.CharField(max_length=120,null=True,blank=True)

# difference between null, blank- https://stackoverflow.com/a/60598009/7857541

    objects = BillingProfileManager()

    def __str__(self):
        return self.email

def billing_profile_create_receiver(sender, instance, *args, **kwargs):
    if not instance.customer_id and instance.email:
        customer = stripe.Customer.create(
            email = instance.email
        )
        instance.customer_id = customer.id

pre_save.connect(billing_profile_create_receiver, sender=BillingProfile)

def post_save_user_created(sender, instance, created, *args, **kwargs):
    if created and instance.email:
        BillingProfile.objects.get_or_create(user=instance, email=instance.email)

# instead of User, using settings.AUTH_USER_MODEL because we are using the custom user model, suggested by djagno
post_save.connect(post_save_user_created, sender=settings.AUTH_USER_MODEL)