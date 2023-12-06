


from datetime import timezone

from django.forms import ModelForm
from django import forms

from account.model import Service

class AcceptRequest(forms.ModelForm):
    class Meta:
        model = Service


    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get('status')

        if status == 'Accepted':
            cleaned_data['dateAccepted'] = timezone.now()


        if status == 'Completed':
            cleaned_data['dateFinished'] = timezone.now()

        return cleaned_data