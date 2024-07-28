from django.contrib import admin
from .models import *
# Register your models here.


@admin.register(dataDeletionModel)
class DocumentModelAdmin(admin.ModelAdmin):
    list_display = ["id","user","reason","additional_info","timestamp"]

@admin.register(Meeting)
class DocumentModelAdmin(admin.ModelAdmin):
    list_display = ["id","user","date","time","timezone","location","reason","description","created_at"]
