from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.HomePageView.as_view(), name='homepage'),
    # path('registerpage/', views.RegisterWorker.as_view(), name='registerpage'),
    # path('login/', views.LoginWorker.as_view(), name='login'),
    path('posting/', views.PostServiceWorker.as_view(), name='posting'),
    path('querypostservice/', views.QueryPostServiceView.as_view(), name='querypostservice'),
    path('deletepostservice/', views.DeletePostService.as_view(), name='deletepostservice'),
    path('updatepostservice/<int:postID>/', views.UpdatePostService.as_view(), name='updatepostservice'),
    # path('httpregister/', views.registration, name='httpregister'),

    path('logout/', LogoutView.as_view(), name='logout'),

]