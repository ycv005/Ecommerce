from django.db import models
from django import forms
from django.contrib.auth.models import User

# Create your models here.

class ContactForm(forms.Form):
    fullname = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control","id":"form_full_name"})) 
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class":"form-control"}))
    content = forms.CharField(widget=forms.Textarea(attrs={"class":"form-control"}))

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not ".com" in email:
            raise forms.ValidationError("Enter correct mail")
        return email