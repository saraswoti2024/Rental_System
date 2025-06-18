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
    path('landlord_home/',landlord_home,name="landlord_home"),
    path('landlord_Dashboard/',landlord_dashboard,name="ldashboard"),
    path('deleteproperty/<int:id>',delete_property,name="deleteproperty"),
    path('house/',house,name="house"),
    path('flat/',flat,name="flat"),
    path('office/',officespace,name="office"),
    path('Room/',Room,name="room"),
    path('land/',land,name="land"),
    path('shutter/',shutter,name="shutter"),
    path('edit_ldashboard/',edit_ldashboard,name="edit_ldashboard"),
]
