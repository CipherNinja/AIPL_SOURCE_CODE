from django.contrib import admin
from .models import CampusConnect

class CampusConnectAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone_number', 'institution_name', 'city', 'state', 'country')
    search_fields = ('full_name', 'email', 'phone_number', 'institution_name', 'city', 'state', 'country')
    list_filter = ('gender', 'city', 'state', 'country', 'institution_name')
    fieldsets = (
        ('Personal Information', {
            'fields': ('full_name', 'date_of_birth', 'gender', 'street', 'city', 'state', 'country', 'zip_code', 'email', 'phone_number')
        }),
        ('Institution Information', {
            'fields': ('institution_name', 'institution_address', 'institution_city', 'institution_state', 'institution_country', 'institution_postal_code')
        }),
    )
    

admin.site.register(CampusConnect, CampusConnectAdmin)
