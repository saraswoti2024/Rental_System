from django.contrib import admin
from .models import *
# Register your mocdels here.

admin.site.register(Choice1)

@admin.register(property_post)
class Featured(admin.ModelAdmin):
    list_display = ['title','address','property_type','price']