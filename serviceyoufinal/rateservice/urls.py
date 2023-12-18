# urls.py
from django.urls import path
from .views import EnterClientID, RateService

urlpatterns = [
    path('', EnterClientID.as_view(), name='enter_client_id'),
    path('rate-service/<int:client_id>/', RateService.as_view(), name='rate_service'),
    # Add other URL patterns as needed
]
