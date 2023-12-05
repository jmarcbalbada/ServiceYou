from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse


# Create your views here.
def landingPage(request):
    return HttpResponse("Welcome to landing page!")
