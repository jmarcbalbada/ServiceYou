# views.py
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, reverse
from django.views import View
from django.db import connection
from django.contrib import messages
from .form import EnterClientIDForm, RateServiceForm  # Import RateServiceForm
from .models import Client, ServiceRequest, RateService


class EnterClientID(View):
    template_name = 'rateservice.html'

    def get(self, request):
        form = EnterClientIDForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = EnterClientIDForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            try:
                client = Client.objects.get(username=username, password=password)
            except Client.DoesNotExist:
                error_message = "Invalid username or password. Please try again."
                return render(request, self.template_name, {'form': form, 'error_message': error_message})

            return redirect('rate_service', client_id=client.clientID)

        return render(request, self.template_name, {'form': form})


class RateService(View):
    template_name = 'rating.html'

    def get(self, request, client_id):
        # Get unrated service requests with status other than 'Pending'
        unrated_service_requests = ServiceRequest.objects.filter(
            clientID=client_id,
            status__in=['Completed', 'Cancelled'],
            rateservice__isnull=True  # Assuming 'rateservice' is the related name in ServiceRequest
        )

        user_id = client_id
        if user_id:
            user = Client.objects.get(pk=user_id)
            firstname = user.firstName if user else None

        # Check if there are no unrated service requests
        if not unrated_service_requests.exists():
            error_message = "No requests to be rated."
            return render(request, 'client_dashboard.html', {'error_message': error_message, 'firstname': firstname})

        # Create a list of tuples for the drop-down menu
        request_choices = [(request.requestID, str(request)) for request in unrated_service_requests]

        # Pass the choices to the form
        form = RateServiceForm(request_choices=request_choices)

        return render(request, self.template_name, {'form': form, 'client_id': client_id})

    def post(self, request, client_id):
        rate_service_form = RateServiceForm(request.POST)

        if rate_service_form.is_valid():
            print(rate_service_form.cleaned_data)
            rate_service = rate_service_form.save(commit=False)
            with connection.cursor() as cursor:
                cursor.callproc('RateService', [rate_service.requestID,
                                                rate_service.rateValue, rate_service.comment])

            # Redirect to the enter-client-id view on success
            return HttpResponseRedirect(reverse('client_dashboard'))

        # If the form is not valid, show an error popup
        return render(request, self.template_name,
                      {'form': rate_service_form, 'client_id': client_id, 'error_popup': True})