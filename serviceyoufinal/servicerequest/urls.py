from django.urls import path
from . import views

urlpatterns = [
    path('servicerequest/', views.ServiceRequest.as_view(), name='servicerequest'),
]