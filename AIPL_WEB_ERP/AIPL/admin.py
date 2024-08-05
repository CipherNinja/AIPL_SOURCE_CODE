from django.contrib import admin
from .models import *
# Register your models here.


@admin.register(dataDeletionModel)
class DocumentModelAdmin(admin.ModelAdmin):
    list_display = ["id","user","reason","additional_info","timestamp"]

@admin.register(Meeting)
class DocumentModelAdmin(admin.ModelAdmin):
    list_display = ["id","user","date","time","location","reason","description"]



class NotificationAdmin(admin.ModelAdmin):
    list_display = ('sender', 'get_recipient_names', 'message', 'timestamp', 'is_read')
    
    def get_recipient_names(self, obj):
        return obj.get_recipient_names()
    get_recipient_names.short_description = 'Recipients'

admin.site.register(Notification, NotificationAdmin)