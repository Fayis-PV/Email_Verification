from django import forms
from django.contrib.auth.models import User
from allauth.account.forms import SignupForm

class CustomSignupForm(SignupForm):
    def clean_email(self):
        response = super().clean_email()
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already taken. Please use a different email.")
        return response

    
