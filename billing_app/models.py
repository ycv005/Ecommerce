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
    
    def charge(self,order_obj, card=None):
        return Charge.objects.makeCharge(self,order_obj,card)

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

class CardManager(models.Manager):
    def all(self, *args, **kwargs): # ModelKlass.objects.all() --> ModelKlass.objects.filter(active=True)
        return self.get_queryset().filter(active=True)

    def add_new(self, billing_profile, token):
        if token:
            customer = stripe.Customer.retrieve(billing_profile.customer_id)
            stripe_card_response = customer.sources.create(source=token)
            new_card = self.model(
                    billing_profile=billing_profile,
                    stripe_id = stripe_card_response.id,
                    brand = stripe_card_response.brand,
                    country = stripe_card_response.country,
                    exp_month = stripe_card_response.exp_month,
                    exp_year = stripe_card_response.exp_year,
                    last4 = stripe_card_response.last4
                )
            new_card.save()
            return new_card
        return None

class Card(models.Model):
    billing_profile = models.ForeignKey(BillingProfile,on_delete=models.CASCADE)
    stripe_id = models.CharField(max_length=120)
    brand = models.CharField(max_length=40,null=True,blank=True)
    country = models.CharField(max_length=20,null=True,blank=True)
    exp_month = models.IntegerField(null=True,blank=True)
    exp_year = models.IntegerField(null=True,blank=True)
    last4 = models.CharField(max_length=4,null=True,blank=True)
    default = models.BooleanField(default=True)

    objects = CardManager()

    def __str__(self):
        return "{} {}".format(self.brand,self.last4)

class ChargeManager(models.Manager):
    def makeCharge(self,billing_profile, order_obj, card=None):
        card_obj = card
        if card_obj is None:
			# _set is used for reverse lookup, https://docs.djangoproject.com/en/3.0/topics/db/queries/#related-objects
            cards = billing_profile.card_set.filter(default=True)
            if cards.exists():
                card_obj = card.first()
        if card_obj is None:
            return False, "No Cards Available"

        c = stripe.Charge.create(
        	amount=order_obj.total,
        	currency="inr",
        	source=card_obj.stripe_id,
        	customer=billing_profile.customer_id,
        	metadata={"order_id":order_obj.order_id}
        	)
        new_charge_obj = self.model(
                    billing_profile = billing_profile,
                    stripe_id = c.id,
                    paid = c.paid,
                    refunded = c.refunded,
                    outcome = c.outcome,
                    outcome_type = c.outcome.get('type'),
                    seller_message = c.outcome.get('seller_message'),
                    risk_level = c.outcome.get('risk_level'),
            )
        new_charge_obj.save()
        return new_charge_obj.paid, new_charge_obj.seller_message

class Charge(models.Model):
    billing_profile         = models.ForeignKey(BillingProfile, on_delete=models.CASCADE)
    stripe_id               = models.CharField(max_length=120)
    paid                    = models.BooleanField(default=False)
    refunded                = models.BooleanField(default=False)
    outcome                 = models.TextField(null=True, blank=True)
    outcome_type            = models.CharField(max_length=120, null=True, blank=True)
    seller_message          = models.CharField(max_length=120, null=True, blank=True)
    risk_level              = models.CharField(max_length=120, null=True, blank=True)

    objects = ChargeManager()