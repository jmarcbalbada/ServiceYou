from django.urls import path
from . import views

urlpatterns = [
    path('acceptservice/', views.acceptservice, name='acceptservice'),
]