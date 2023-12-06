from django.forms import ModelForm
from django import forms

from serviceyoufinal.account.models import *


class ServiceRequestForm(forms.ModelForm):
    class Meta:
        model = ServiceRequest
        fields = ['clientID', 'workerID', 'serviceID', 'requestDate', 'status', 'dateAccepted', 'dateFinished']
