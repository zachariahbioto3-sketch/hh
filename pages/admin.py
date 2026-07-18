from django.contrib import admin
from .models import ContactMessage

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display  = ('name','email','subject','submitted_at','read')
    list_filter   = ('read',)
    list_editable = ('read',)
