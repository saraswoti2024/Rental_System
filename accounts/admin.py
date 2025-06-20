from django.contrib import admin
from .models import *

@admin.register(CustomUser)
class User_data(admin.ModelAdmin):
    list_display = ['id','username','usertype','is_superuser','email','last_login']

    