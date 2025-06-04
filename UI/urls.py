from django.urls import path
from .views import *
urlpatterns = [
    path('home/',HomeView.as_view(),name='home'),
    path('choices/',choices,name="choices"),
    path('choices/',common,name='common'),
]
