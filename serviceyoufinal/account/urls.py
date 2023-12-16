from django.urls import path
from . import views

urlpatterns = [
    path('', views.LoginPageView.as_view(), name='landingpage'),
    path('home_client', views.clientPage, name='home_client'),
    # path('request-service/', views.ClientRequestServiceView.as_view(), name='request_service'),
    # path('pay-service/', views.ClientPayServiceView.as_view(), name='pay_service'),
    # path('rate-service/', views.ClientRateServiceView.as_view(), name='rate_service'),
    # path('client-dashboard/', views.ClientDashboardView.as_view(), name='client_dashboard'),
]