from .models import AddressModel
from django import forms

class AddressForm(forms.ModelForm):
    class Meta:
        model = AddressModel
        fields ='__all__'
        exclude = [
            'billing_profile'
        ]
