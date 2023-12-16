from django.forms import ModelForm
from django import forms
from .models import RateService

class RateServiceForm(ModelForm):
    class Meta:
        model = RateService
        fields = ['requestID', 'rateValue', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'placeholder': 'Enter your comment here...'}),
        }

    def __init__(self, *args, **kwargs):
        request_choices = kwargs.pop('request_choices', None)
        super(RateServiceForm, self).__init__(*args, **kwargs)

        if request_choices:
            self.fields['requestID'].choices = request_choices


class EnterClientIDForm(forms.Form):
    username = forms.CharField(max_length=10)
    password = forms.CharField(max_length=10, widget=forms.PasswordInput)

