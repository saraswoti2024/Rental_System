from django.contrib import admin
from .models import *
# Register your mocdels here.

@admin.register(property_post)
class Featured(admin.ModelAdmin):
    list_display = ['title','address','property_type','price','is_approved']
    list_filter = ['is_approved'] #side bar auxa filter garerw herna yes,no wala
    list_editable = ['is_approved'] #direct tick button aauxa bahirw nai vitrw thichi rakhnu pardaian


