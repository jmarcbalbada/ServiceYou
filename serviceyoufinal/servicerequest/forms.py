from datetime import timezone

from django.forms import ModelForm
from django import forms

from .models import ServiceRequest

class ServiceRequestForm(forms.ModelForm):
    class Meta:
        model = ServiceRequest
        fields = ['clientID', 'workerID', 'serviceID', 'requestDate', 'status', 'dateAccepted', 'dateFinished']

    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get('status')

        if status == 'Accepted':
            cleaned_data['dateAccepted'] = timezone.now()


        if status == 'Completed':
            cleaned_data['dateFinished'] = timezone.now()

        return cleaned_data