from django.urls import path
from . import views

urlpatterns = [
    path('rating/', views.RateService.as_view(), name='rating'),
    path('', views.rating, name='temp'),
]
