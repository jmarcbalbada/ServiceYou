from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.urls import reverse
from django.contrib import messages
from .models import *

#
# # Create your views here.
def landingPage(request):
    return HttpResponse("Welcome to landing page!")


def clientPage(request):
    return HttpResponse("You are a client!")


def workerPage(request):
    return HttpResponse("You are a worker!")

class WorkerPageView(View):
    template = '../postservice/home.html'

    def get(self,request):
        postservice_url = reverse('') # your url HERE
        return redirect(postservice_url)


class LoginPageView(View):
    template = 'login.html'

    def get(self, request):
        return render(request, self.template)

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Attempt to authenticate as a Worker
        worker = Worker.authenticate_worker(username, password)
        if worker is not None:
            # Log in the worker
            request.session['user_id'] = worker.workerID
            return redirect('postservice/')  # Redirect to the worker's home page

        # If not a Worker, attempt to authenticate as a Client
        client = Client.authenticate_client(username, password)
        if client is not None:
            # Log in the client
            request.session['user_id'] = client.clientID
            return redirect('home_client')  # Redirect to the client's home page

        # Authentication failed, handle accordingly (e.g., display an error message)
        return render(request, self.template, {'error_message': 'Invalid credentials'})
