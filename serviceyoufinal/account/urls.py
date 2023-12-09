from django.urls import path
from . import views

urlpatterns = [
    path('', views.LoginPageView.as_view(), name='landingpage'),
    path('home_client', views.clientPage, name='home_client'),
]