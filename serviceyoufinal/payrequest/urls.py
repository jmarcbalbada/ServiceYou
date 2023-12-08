from django.urls import path
from . import views

urlpatterns = [
    path('payment/', views.PayFormView.as_view(), name = 'payment'),
]