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

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class RegisterForm(forms.Form):
    email = forms.EmailField()
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password",widget=forms.PasswordInput)

    def clean(self):
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password2 != password:
            raise forms.ValidationError("Password Not Match")
        return self.cleaned_data

    def clean_username(self):
        username = self.cleaned_data.get("username") 
        qs = User.objects.filter(username=username)
        if qs.exists():
            raise forms.ValidationError("User Already Exist, Go to Login")
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get("email") 
        qs = User.objects.filter(username=email)
        if qs.exists():
            raise forms.ValidationError("Email Already Exist, Go to Login")
        return email