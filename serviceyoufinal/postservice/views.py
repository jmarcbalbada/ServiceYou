from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth import get_user_model
from .form import *


# Create your views here.

def registration(request):
    return HttpResponse("Register page")


def homePage(request):
    return HttpResponse("Home page")


class HomePageView(View):
    template = 'home.html'
    registerRedirect = 'registerpage'
    loginRedirect = 'login'

    def get(self, request):
        return render(request, self.template)

    def register(self, request):
        # Redirect to the 'register.html' page
        return HttpResponseRedirect(reverse('registerpage'))

    def login(self, request):
        # Redirect to the 'login.html' page
        return HttpResponseRedirect(reverse('login'))


class PostServiceWorker(View):
    template = 'postserviceworker.html'

    def get(self, request):
        postService = PostServiceWorkerForm()
        return render(request, self.template, {'form': postService})


class RegisterWorker(View):
    template = 'register.html'
    nextPageTemplate = 'login.html'

    def get(self, request):
        worker = RegisterForm()
        return render(request, self.template, {'form': worker})

    def post(self, request):
        worker = RegisterForm(request.POST)
        if worker.is_valid():
            worker.save()
            # proceed to login page
            return HttpResponseRedirect(reverse('login'))
        else:
            # Something went wrong
            messages.error(request, 'Something went wrong. Please try again.')
            return render(request, self.template, {'form': worker})


class LoginWorker(View):
    template = 'login.html'

    def get(self, request):
        worker = LoginForm()
        return render(request, self.template, {'form': worker})

    def post(self, request):
        worker = LoginForm(request.POST)
        if worker.is_valid():
            worker_id = worker.cleaned_data.get('worker_id')
            password = worker.cleaned_data.get('password')

            User = get_user_model()

            try:
                worker = User.objects.get(workerId=worker_id)
            except User.DoesNotExist:
                worker = None

            if worker is not None and worker.check_password(password):
                # Authentication was successful, so log in the user
                login(request, worker)
                # Redirect to a success page or the user's profile page
                return HttpResponseRedirect(reverse('profile'))  # Replace 'profile' with your desired URL name
            else:
                # Authentication failed, show an error message
                messages.error(request, 'Invalid worker ID or password.')
        else:
            # Form validation failed, show an error message
            messages.error(request, 'Please correct the form errors.')

        return render(request, self.template, {'form': worker})

# class LoginWorker(View):
#     template = 'login.html'
#
#     def get(self, request):
#         worker = LoginForm()
#         return render(request, self.template, {'form': worker})
#
#     def post(self, request):
#         worker = LoginForm(request.POST)
#         if worker.is_valid():
#             worker.save()
#             # proceed to login page
#             return render(request, self.template, {'form': worker})
#         else:
#             # Something went wrong
#             return render(request, self.template, {'form': worker})