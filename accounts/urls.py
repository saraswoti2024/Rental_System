from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *
urlpatterns = [
    path('login/',Log_in.as_view(),name="log_in"),
    path('register1/',Register1.as_view(),name="register1"),
    path('Logout/',log_out,name="log_out"),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
