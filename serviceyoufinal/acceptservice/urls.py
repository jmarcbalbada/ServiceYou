from django.urls import path
from . import views

urlpatterns = [
    path('acceptservice/', views.acceptservice, name='acceptservice'),
    path('pendingservice/', views.pendingservice, name='pendingservice'),
    path('completedservice/', views.completedservice, name='completedservice'),
    path('failedservice/', views.failedservice, name='failedservice'),
    path('cancelledservice/', views.cancelledservice, name='cancelledservice'),
]