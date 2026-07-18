from django.contrib import admin
from django.utils.html import format_html
from .models import ContactMessage, Executive


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject", "submitted_at")
    search_fields = ("name", "email", "message")


@admin.register(Executive)
class ExecutiveAdmin(admin.ModelAdmin):
    list_display = ("photo_preview", "name", "position", "order", "is_active")
    list_editable = ("order", "is_active")
    list_display_links = ("name",)
    search_fields = ("name", "position")
    ordering = ("order", "name")

    def photo_preview(self, obj):
        if obj.photo:
            return format_html(
                '<img src="{}" style="height:42px;width:42px;border-radius:50%;object-fit:cover;" />',
                obj.photo.url,
            )
        return "-"
    photo_preview.short_description = "Photo"
