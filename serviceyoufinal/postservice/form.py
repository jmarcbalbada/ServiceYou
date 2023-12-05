from django.forms import ModelForm
from django import forms
from django.forms.widgets import PasswordInput
from account.models import Worker, Service


class RegisterForm(ModelForm):
    workerId = forms.CharField(widget=forms.TextInput)
    username = forms.CharField(widget=forms.TextInput)
    password = forms.CharField(widget=PasswordInput(attrs={'type': 'password'}))
    firstName = forms.CharField(widget=forms.TextInput)
    lastName = forms.CharField(widget=forms.TextInput)
    middleName = forms.CharField(widget=forms.TextInput)
    phoneNo = forms.CharField(widget=forms.TextInput)
    email = forms.EmailField()
    address = forms.CharField(widget=forms.TextInput)

    class Meta:
        model = Worker
        fields = ['workerId', 'username', 'password', 'firstName', 'lastName', 'phoneNo', 'email',
                  'address']
        labels = {
            'workerId': 'Worker ID',
            'username': 'Username',
            'password': 'Password',
            'firstName': 'First Name',
            'lastName': 'Last Name',
            'phoneNo': 'Phone Number',
            'email': 'Email',
            'address': 'Address',
        }
        # fields = '__all__'


class LoginForm(forms.Form):
    workerId = forms.CharField(widget=forms.TextInput)
    password = forms.CharField(widget=forms.PasswordInput)


class PostServiceWorkerForm(forms.Form):
    workerId = forms.CharField(label="Worker ID", widget=forms.TextInput, required=True)
    serviceType = forms.CharField(label="Service Type", widget=forms.TextInput, required=True)
