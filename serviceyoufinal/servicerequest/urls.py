from django.urls import path
from . import views

urlpatterns = [
    path('servicerequest/', views.ServiceRequest.as_view(), name='servicerequest'),
    path('servicerequest/<int:request_id>/', views.ServiceRequest.as_view(), name='service_request_detail'),
]