from django.urls import path
from .views import *
urlpatterns = [
    path('login/',Log_in.as_view(),name="log_in"),
    path('register/',Register.as_view(),name="register")
]
