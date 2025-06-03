from django.urls import path
from .views import *
urlpatterns = [
    path('login/',Log_in.as_view(),name="log_in"),
    path('register1/',Register1.as_view(),name="register1"),
    path('register2/',Register2.as_view(),name="register2")
]
