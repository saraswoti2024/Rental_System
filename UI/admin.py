from django.contrib import admin
from .models import *
# Register your mocdels here.

@admin.register(property_post)
class Featured(admin.ModelAdmin):
    list_display = [field.name for field in property_post._meta.fields]
    list_filter = ['is_approved'] #side bar auxa filter garerw herna yes,no wala
    list_editable = ['is_approved'] #direct tick button aauxa bahirw nai vitrw thichi rakhnu pardaian

@admin.register(ShiftHome)
class Shift_Home(admin.ModelAdmin):
    list_display = [field.name for field in ShiftHome._meta.fields]

@admin.register(RequestRoom)
class request_room(admin.ModelAdmin):
    list_display = [field.name for field in RequestRoom._meta.fields]

from django.contrib import admin
from .models import ActivityLog

@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ['id','user', 'action', 'timestamp']
    list_filter = ['user', 'timestamp']
    search_fields = ['action', 'user__username']
    ordering = ['-timestamp']

@admin.register(Fraud_Reports)
class Fraud_Report(admin.ModelAdmin):
    list_display = ['id','reporter_id', 'property_name', 'message', 'timestamp']
    list_filter = ['property_name', 'reporter_id','timestamp']
    search_fields = ['reporter_id', 'property_name__title', 'message']

    def message_preview(self, obj):
        return obj.message[:50] + ('...' if len(obj.message) > 50 else '')
    message_preview.short_description = "Message"
    
@admin.register(Testimonals)
class Testimonals(admin.ModelAdmin):
    list_display = ['id','name','comment']