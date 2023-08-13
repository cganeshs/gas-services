from django.contrib import admin
from django.urls import path,include
from .views import *



urlpatterns = [
    path('register', CustomerRegistrationView),
    path('login/', CustomAuthToken.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('service-request/',ServiceRequestView.as_view({'get': 'list', 'post':'create'}))
]