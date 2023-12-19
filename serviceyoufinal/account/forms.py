from django import forms
from .models import Worker

class WorkerRegistrationForm(forms.ModelForm):
    class Meta:
        model = Worker
        fields = ['username', 'password', 'firstName', 'lastName', 'address', 'phoneNo', 'email']
        widgets = {
            'password': forms.PasswordInput(),  # Renders the password field as a password input
        }
