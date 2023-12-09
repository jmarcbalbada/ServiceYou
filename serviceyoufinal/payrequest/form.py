from django.forms import ModelForm
from django import forms
from account.models import *


class PayForm (forms.ModelForm):

    class Meta:
        model = Payment
        exclude = ['amountDue','status']
        fields = ['requestID', 'clientID', 'workerID', 'amount', 'paymentDate','amountDue','amountPaid','status']