from django.contrib import admin
from django.utils.html import format_html
from .models import CampusConnect

class CampusConnectAdmin(admin.ModelAdmin):
    list_display = (
        'full_name', 
        'phone_number', 
        'email', 
        'status',
        'call_button',
        'email_button',
        'whatsapp_button',
        'remark'
    )

    def call_button(self, obj):
        # Generate a button that links to a phone call
        return format_html(
            '<a class="button" href="tel:{}" style="color: green; text-decoration: none; font-weight: bold;">📞 Call</a>',
            obj.phone_number
        )
    call_button.short_description = "Call"

    def email_button(self, obj):
        # Generate a button that links to the email client
        return format_html(
            '<a class="button" href="mailto:{}" style="color: blue; text-decoration: none; font-weight: bold;">✉️ Email</a>',
            obj.email
        )
    email_button.short_description = "Email"

    def whatsapp_button(self, obj):
        whatsapp_link = f"https://wa.me/{obj.phone_number}"
        return format_html(
            '<a class="button" href="{}" target="_blank" style="color: green; text-decoration: none; font-weight: bold;">💬 WhatsApp</a>',
            whatsapp_link
        )
    whatsapp_button.short_description = "WhatsApp"

admin.site.register(CampusConnect, CampusConnectAdmin)
