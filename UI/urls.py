from django.urls import path
from .views import *
urlpatterns = [
    path('home/',HomeView.as_view(),name='home'),
    path('choices/',choices,name="choices"),
    path('choices/',common,name='common'),
    path('request/',request_room_view,name="request_room"),
    path('shift_home/',shifthome,name="shifthome"),
    path('aboutus/',aboutus,name="aboutus"),
    path('addproperty/',addproperty,name="addproperty"),
]
