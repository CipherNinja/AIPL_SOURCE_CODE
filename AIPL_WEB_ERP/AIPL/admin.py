from django.contrib import admin
from .models import *
# Register your models here.


@admin.register(dataDeletionModel)
class DocumentModelAdmin(admin.ModelAdmin):
    list_display = ["id","user","reason","additional_info","timestamp"]
