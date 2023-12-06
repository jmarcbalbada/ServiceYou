from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from .form import RateServiceForm


# Create your views here.

def rating(request):
    return HttpResponse("SUCCESS!")


class RateService(View):
    template = 'rating.html'

    def get(self, request):
        score = RateServiceForm()
        return render(request, self.template, {'form': score})