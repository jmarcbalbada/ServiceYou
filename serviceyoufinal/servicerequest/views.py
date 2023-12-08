from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views import View
from .forms import ServiceRequestForm
from django.db import connection

class ServiceRequest(View):
    template = 'servicerequest.html'

    def get(self, request, request_id=None):
        # If request_id is provided, retrieve the service request
        if request_id is not None:
            with connection.cursor() as cursor:
                cursor.callproc('GetServiceRequest', [request_id])
                result = cursor.fetchone()

            service_form = ServiceRequestForm(initial={
                'clientID': result[0],
                'workerID': result[1],
                'serviceID': result[2],
                'requestDate': result[3],
                'status': result[4],
                'dateAccepted': result[5],
                'dateFinished': result[6],
            })
        else:
            service_form = ServiceRequestForm()

        return render(request, self.template, {'form': service_form})

    def post(self, request, request_id=None):
        service = ServiceRequestForm(request.POST)
        if service.is_valid():
            service_instance = service.save(commit=False)
            service_instance.save()
        return render(request, self.template, {'form': service})

    def put(self, request, request_id):
        service = ServiceRequestForm(request.POST)
        if service.is_valid():
            status = service.cleaned_data['status']
            date_accepted = service.cleaned_data['dateAccepted']
            date_finished = service.cleaned_data['dateFinished']

            with connection.cursor() as cursor:
                cursor.callproc('UpdateServiceRequest', [request_id, status, date_accepted, date_finished])

            return render(request, self.template, {'form': service})

    def delete(self, request, request_id):
        with connection.cursor() as cursor:
            cursor.callproc('DeleteServiceRequest', [request_id])

        return HttpResponse(status=204)
