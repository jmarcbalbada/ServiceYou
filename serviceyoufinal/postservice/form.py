from django import forms
from account.models import Worker, Service
from .models import PostService


class PostServiceForm(forms.ModelForm):
    class Meta:
        model = PostService
        fields = ['workerID', 'serviceID', 'title', 'description', 'location']
