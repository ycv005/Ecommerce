from django.db import models

from billing_app.models import BillingProfile
from django.core.validators import MaxValueValidator

class AddressModel(models.Model):
    # want to have many address to a billing profile
    billing_profile = models.ForeignKey(BillingProfile, on_delete=models.CASCADE)
    address_line_1 = models.CharField(max_length=150)
    address_line_2 = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    postal_code = models.IntegerField(validators=[MaxValueValidator(999999)]) #value won't be greater than 6 digit

    def __str__(self):
        return str(self.billing_profile)

    def get_address(self):
        return ("{line_1}, {line_2}, {city}, {state}, {country}".format(
            line_1 = self.address_line_1,
            line_2 = self.address_line_2 or "",
            city = self.city,
            state = self.state,
            country = self.country
        ))