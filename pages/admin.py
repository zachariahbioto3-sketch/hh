from django.contrib import admin
from .models import ContactMessage, Officer

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display  = ('name', 'email', 'subject', 'submitted_at', 'read')
    list_filter   = ('read',)
    ordering      = ('-submitted_at',)

@admin.register(Officer)
class OfficerAdmin(admin.ModelAdmin):
    list_display  = ('order', 'name', 'position', 'term', 'is_active')
    list_display_links = ('name')
    list_editable = ('order', 'is_active')
