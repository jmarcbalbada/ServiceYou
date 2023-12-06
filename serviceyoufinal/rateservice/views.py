from django.http import HttpResponse
from django.shortcuts import render
from django.db import connection
from django.views import View
from .form import RateServiceForm


def rating(request):
    return HttpResponse("SUCCESS!")


class RateService(View):
    template = 'rating.html'

    def get(self, request):
        score = RateServiceForm()
        return render(request, self.template, {'form': score})

    def post(self, request):
        rateServiceForm = RateServiceForm(request.POST)

        if rateServiceForm.is_valid():
            rateService = rateServiceForm.save(commit=False)

            with connection.cursor() as cursor:
                cursor.callproc('RateService', [rateService.requestID,
                                rateService.rateValue, rateService.comment])

            return render(request, self.template, {'form': RateServiceForm()})
        else:
            return render(request, self.template, {'form': rateServiceForm})
