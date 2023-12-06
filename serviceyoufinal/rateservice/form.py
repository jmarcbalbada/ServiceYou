from django.forms import ModelForm
from django import forms
from .models import RateService


class RateServiceForm(ModelForm):

    class Meta:
        model = RateService
        fields = ['requestID', 'rateValue', 'comment']