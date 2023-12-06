from django.shortcuts import render
from django.views import View
from .forms import *
# Create your views here.
class ServiceRequest(View):
    template = 'servicerequest.html'

    def get(self, request):
        service = ServiceRequestForm()
        return render(request, self.template, {'form': service})

    def post(self, request):
        service = ServiceRequestForm(request.POST)
        if service.is_valid():
            service_instance = service.save(commit=False)
            service_instance.save()
        return render(request, self.template, {'form': service})
